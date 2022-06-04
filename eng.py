import tensorflow as tf
from tqdm import tqdm
import transformers
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, BertConfig
from transformers import BertForSequenceClassification
from tqdm import tqdm, trange
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt
from zemberek import (
    TurkishSpellChecker,
    TurkishSentenceNormalizer,
    TurkishSentenceExtractor,
    TurkishMorphology,
    TurkishTokenizer
)
from gensim import utils
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import torch.nn as nn
from transformers import BertModel
import torch.nn.functional as F
import pickle

class BertClassifier(nn.Module):
    def __init__(self, freeze_bert=False):
        super(BertClassifier, self).__init__()
        # Specify hidden size of BERT, hidden size of our classifier, and number of labels
        D_in, H, D_out = 768, 64, 3

        # Instantiate BERT model
        self.bert = BertModel.from_pretrained('dbmdz/bert-base-turkish-128k-cased')

        # Instantiate an one-layer feed-forward classifier
        self.classifier = nn.Sequential(
            nn.Linear(D_in, 256),
            nn.GELU(),
            nn.Linear(256, H),
            nn.GELU(),
            #nn.Dropout(0.5),
            nn.Linear(H, D_out)
        )

        # Freeze the BERT model
        if freeze_bert:
            for param in self.bert.parameters():
                param.requires_grad = False
        
    def forward(self, input_ids, attention_mask):
        # Feed input to BERT
        outputs = self.bert(input_ids=input_ids,
                            attention_mask=attention_mask)
        
        # Extract the last hidden state of the token `[CLS]` for classification task
        last_hidden_state_cls = outputs[0][:, 0, :]

        # Feed input to classifier to compute logits
        logits = self.classifier(last_hidden_state_cls)

        return logits


class Controller():

    stopwordList = []
    tokenizer = BertTokenizer.from_pretrained('dbmdz/bert-base-turkish-128k-cased', do_lower_case=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __init__(self):        
        self.n_gpu = torch.cuda.device_count()
        torch.cuda.get_device_name(0)

        with open("stopwords.txt","r") as file:
            stopwordList = file.readlines()

        for i in range(len(stopwordList)):
            stopwordList[i] = stopwordList[i].replace("\n","")

        with open("model.pickle","rb") as f:
            self.bert_classifier = pickle.load(f)

    def tknz(self,inp, token_min_len=2, token_max_len=100, lower=True, stopwordList = stopwordList):
        lowerMap = {ord(u'A'): u'a',ord(u'A'): u'a',ord(u'B'): u'b',ord(u'C'): u'c',ord(u'Ç'): u'ç',ord(u'D'): u'd',ord(u'E'): u'e',ord(u'F'): u'f',ord(u'G'): u'g',ord(u'Ğ'): u'ğ',ord(u'H'): u'h',ord(u'I'): u'ı',ord(u'İ'): u'i',ord(u'J'): u'j',ord(u'K'): u'k',ord(u'L'): u'l',ord(u'M'): u'm',ord(u'N'): u'n',ord(u'O'): u'o',ord(u'Ö'): u'ö',ord(u'P'): u'p',ord(u'R'): u'r',ord(u'S'): u's',ord(u'Ş'): u'ş',ord(u'T'): u't',ord(u'U'): u'u',ord(u'Ü'): u'ü',ord(u'V'): u'v',ord(u'Y'): u'y',ord(u'Z'): u'z'}
        inp = inp.translate(lowerMap)
        tokenizer = TurkishTokenizer.DEFAULT
        tknL = tokenizer.tokenize(inp)
        ## (not str(t.type_) == "Type.Mention") can be added!
        ls = []
        ls.append("[CLS]")
        for t in tknL:
            if (not t.content.startswith("_")) and (not str(t.type_) == "Type.URL") and (not str(t.type_) == "Type.Punctuation") and (not t.content in stopwordList):
                ls.append(utils.to_unicode(t.content))
        ls.append("[SEP]")
        return ls

    def conc(self,inp):
        st = inp[0]
        for s in inp[1:]:
            st += " "
            st += s
        return st

    def prep(self,data):
        input_ids = []
        attention_masks = []

        for sent in data:
            #print(sent)
            encoded_sent = self.tokenizer.encode_plus(
                text=self.conc(self.tknz(sent)),          # Preprocess sentence
                add_special_tokens=False,       # Add `[CLS]` and `[SEP]`
                max_length=64,                 # Max length to truncate/pad
                pad_to_max_length=True,         # Pad sentence to max length
                return_attention_mask=True      # Return attention mask
                )

            input_ids.append(encoded_sent.get('input_ids'))
            attention_masks.append(encoded_sent.get('attention_mask'))
        
        input_ids = torch.tensor(input_ids)
        attention_masks = torch.tensor(attention_masks)
        
        return input_ids, attention_masks

    def bert_predict(self, model, test_dataloader):
        """Perform a forward pass on the trained BERT model to predict probabilities
        on the test set.
        """
        print(self.device)
        # Put the model into the evaluation mode. The dropout layers are disabled during
        # the test time.
        model.eval()

        all_logits = []

        # For each batch in our test set...
        for batch in test_dataloader:
            # Load batch to GPU
            b_input_ids, b_attn_mask = tuple(t.to(self.device) for t in batch)[:2]

            # Compute logits
            with torch.no_grad():
                logits = model(b_input_ids, b_attn_mask)
            all_logits.append(logits)
        
        # Concatenate logits from each batch
        all_logits = torch.cat(all_logits, dim=0)

        # Apply softmax to calculate probabilities
        probs = F.softmax(all_logits, dim=1).cpu().numpy()

        return probs

    def avg_result(self, dat):
        sentences = TurkishSentenceExtractor().from_paragraph(dat)

        inp_id, att_mask = self.prep(sentences)
        test_dataset = TensorDataset(inp_id, att_mask)
        test_sampler = SequentialSampler(test_dataset)
        test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=32)

        out_val = self.bert_predict(self.bert_classifier, test_dataloader)
        res = [0,0,0]
        val = []
        for i in out_val:
            ind = np.argmax(i)
            val.append(ind)
            if(ind == 0):
                res[0] = res[0] + 1
            elif(ind == 2):
                res[1] = res[1] + 1
            else:
                res[2] = res[2] + 1
        
        return res, val


# strk = "Bu arabadan nefret ediyorum. Bugün hava çok güzel. Telefon çok iyi ama bataryası kötü hissettiriyor. hizli teslimat tesekkürler. Enflasyondaki artış nedeniyle alım gücü azaldı."
# con = Controller()
# r, val = con.avg_result(strk)
# print(r)
# print(val)