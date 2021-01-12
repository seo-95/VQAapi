__author__ = 'aagrawal'
__version__ = '0.9'

# Interface for accessing the VQA dataset.

# This code is based on the code written by Tsung-Yi Lin for MSCOCO Python API available at the following link:
# (https://github.com/pdollar/coco/blob/master/PythonAPI/pycocotools/coco.py).

# The following functions are defined:
#  VQA        - VQA class that loads VQA annotation file and prepares data structures.
#  getQuesIds - Get question ids that satisfy given filter conditions.
#  getImgIds  - Get image ids that satisfy given filter conditions.
#  loadQA     - Load questions and answers with the specified question ids.
#  showQA     - Display the specified questions and answers.
#  loadRes    - Load result file and create result object.

# Help on each function can be accessed by: "help(COCO.function)"

import pdb
import json
import datetime
import copy

class VQA:
    def __init__(self, question_file, annotation_file=None, verbose=False):
        """Constructor of VQA helper class for reading and visualizing questions and answers.

        Args:
            question_file (str): location of VQA question file
            annotation_file (str, optional): location of VQA annotation file. If not specified (e.g., during test phase) some methods are not accessible. Defaults to None.
            test_mode (bool, optional): set to True to avoid loading annotations. Defaults to False.
        """
        assert question_file, 'Question file must be always specified'
        self.annotations    = {}
        self.questions  = {}
        self.qa         = {}
        self.qqa        = {}
        self.imgToQA    = {}

        time_t = datetime.datetime.utcnow()
        #annotations
        self.annotations = None #quest_type + img_id + question_id + answers
        self.questions = None #question + image_id + question_id
        if annotation_file:
            if verbose:
                print('loading VQA annotations and questions into memory...')
            self.annotations = json.load(open(annotation_file, 'r'))
        if question_file:
            if verbose:
                print('eval mode: loading only VQA questions into memory...')
            self.questions       = json.load(open(question_file, 'r'))
        if verbose:
            print(datetime.datetime.utcnow() - time_t)
        self.createIndex(verbose)

    def createIndex(self, verbose=False):
        # create index
        if verbose:
            print('creating index...')
        img2QA      = {ann['image_id']:     [] for ann in self.questions['questions']}
        q2a       = {ann['question_id']:  [] for ann in self.questions['questions']}
        q2q       = {ann['question_id']:  [] for ann in self.questions['questions']}
        if self.annotations:
            for ann in self.annotations['annotations']:
                img2QA[ann['image_id']]     += [ann]
                q2a[ann['question_id']]   = ann
        for ques in self.questions['questions']:
            q2q[ques['question_id']]    = ques

        if verbose: 
            print('index created!')
        # create class members
        self.q2a = q2a
        self.q2q = q2q
        self.imgToQA = img2QA        


    def info(self):
        """Print information about the VQA annotation file.
        """
        info = self.questions['info']
        for key, value in info.items():
            print('{}: {}'.format(key, value))


    def getQuesIds(self, imgIds=[], quesTypes=[], ansTypes=[]):
        """Get question ids that satisfy given filter conditions. default skips that filter.

        Args:
            imgIds (list, optional):  get question ids for given imgs. Defaults to [].
            quesTypes (list, optional): get question ids for given question types. Defaults to [].
            ansTypes (list, optional): get question ids for given answer types. Defaults to [].

        Raises:
            NotImplementedError: [description]

        Returns:
            list: integer array of question ids
        """
        if not self.annotations:
            assert not len(ansTypes), 'Annotations are not available, you cannot specify ansTypes for filtering'
        imgIds       = imgIds    if type(imgIds)    == list else [imgIds]
        quesTypes = quesTypes if type(quesTypes) == list else [quesTypes]
        ansTypes  = ansTypes  if type(ansTypes)  == list else [ansTypes]

        if len(imgIds) == len(quesTypes) == len(ansTypes) == 0:
            anns = self.annotations['annotations']
        else:
            if not len(imgIds) == 0:
                anns = sum([self.imgToQA[imgId] for imgId in imgIds if imgId in self.imgToQA],[])
            else:
                 anns = self.annotations['annotations']
            anns = anns if len(quesTypes) == 0 else [ann for ann in anns if ann['question_type'] in quesTypes]
            anns = anns if len(ansTypes)  == 0 else [ann for ann in anns if ann['answer_type'] in ansTypes]
        ids = [ann['question_id'] for ann in anns]
        return ids


    def getImgIds(self, quesIds=[], quesTypes=[], ansTypes=[]):
        """Get image ids that satisfy given filter conditions. default skips that filter.

        Args:
            quesIds (list, optional): get image ids for given question ids. Defaults to [].
            quesTypes (list, optional): get image ids for given question types. Defaults to [].
            ansTypes (list, optional): get image ids for given answer types. Defaults to [].

        Raises:
            NotImplementedError: [description]

        Returns:
            list: integer array of image ids
        """
        if not self.annotations:
            assert not len(ansTypes), 'Annotations are not available, you cannot specify ansTypes for filtering'
        quesIds   = quesIds   if type(quesIds)   == list else [quesIds]
        quesTypes = quesTypes if type(quesTypes) == list else [quesTypes]
        ansTypes  = ansTypes  if type(ansTypes)  == list else [ansTypes]

        if len(quesIds) == len(quesTypes) == len(ansTypes) == 0:
            anns = self.annotations['annotations']
        else:
            if not len(quesIds) == 0:
                anns = sum([self.qa[quesId] for quesId in quesIds if quesId in self.qa],[])
            else:
                anns = self.annotations['annotations']
            anns = anns if len(quesTypes) == 0 else [ann for ann in anns if ann['question_type'] in quesTypes]
            anns = anns if len(ansTypes)  == 0 else [ann for ann in anns if ann['answer_type'] in ansTypes]
        ids = [ann['image_id'] for ann in anns]
        return ids


    def loadQA(self, ids=[]):
        """Load questions and answers with the specified question ids.

        Args:
            ids (list, optional): integer ids specifying question ids. Defaults to [].

        Raises:
            NotImplementedError: [description]

        Returns:
            list: loaded qa objects
        """
        assert self.annotations, 'Annotations not available!'
        if type(ids) == list:
            return [self.q2a[id] for id in ids]
        elif type(ids) == int:
            return [self.q2a[ids]]


    def showQA(self, anns):
        """Display the specified annotations.

        Args:
            anns (list): annotations to display

        Raises:
            NotImplementedError: [description]
        """
            
        assert self.annotations, 'Annotations not available!'
        if len(anns) == 0:
            return 0
        for ann in anns:
            quesId = ann['question_id']
            print("Question: %s" %(self.qqa[quesId]['question']))
            for ans in ann['answers']:
                print("Answer %d: %s" %(ans['answer_id'], ans['answer']))


    def loadRes(self, resFile, quesFile, verbose=False):
        """Load result file and return a result object.

        Args:
            resFile (str): file name of result file
            quesFile (str): file name of question file

        Raises:
            NotImplementedError: [description]

        Returns:
            obj: result api object
        """
        res = VQA(quesFile)
        res.annotations = {}
        res.annotations['info'] = copy.deepcopy(self.questions['info'])
        res.annotations['task_type'] = copy.deepcopy(self.questions['task_type'])
        res.annotations['data_type'] = copy.deepcopy(self.questions['data_type'])
        res.annotations['data_subtype'] = copy.deepcopy(self.questions['data_subtype'])
        res.annotations['license'] = copy.deepcopy(self.questions['license'])
        if verbose:
            print('Loading and preparing results...     ')
        time_t = datetime.datetime.utcnow()
        anns    = json.load(open(resFile))
        assert type(anns) == list, 'results is not an array of objects'
        annsQuesIds = [ann['question_id'] for ann in anns]
        assert set(annsQuesIds) == set(self.getQuesIds()), \
        'Results do not correspond to current VQA set. Either the results do not have predictions for all question ids in annotation file or there is atleast one question id that does not belong to the question ids in the annotation file.'
        for ann in anns:
            quesId                  = ann['question_id']
            if res.annotations['task_type'] == 'Multiple Choice':
                assert ann['answer'] in self.q2q[quesId]['multiple_choices'], 'predicted answer is not one of the multiple choices'
            qaAnn                = self.q2a[quesId]
            ann['image_id']      = qaAnn['image_id']
            ann['question_type'] = qaAnn['question_type']
            ann['answer_type']   = qaAnn['answer_type']
        if verbose:
            print('DONE (t=%0.2fs)'%((datetime.datetime.utcnow() - time_t).total_seconds()))

        res.annotations['annotations'] = anns
        res.createIndex(verbose)
        return res
