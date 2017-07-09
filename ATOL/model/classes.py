#coding:utf-8
#2017 04 30
#ding

#import 

#doc
class doc:

    def __init__(self, title, content, labels):
        self.content = content
        self.title = title
        self.labels = labels

    def setLabels(self, labels):
        self.labels = labels

    def getLabels(self):
        return self.labels

    def getTitle(self):
        return self.title

    def getContent(self):
        return self.content

    def getAll(self):
        return self.getTitle(), self.getContent(), self.getLabels()
