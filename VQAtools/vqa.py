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

import json
import datetime
import copy

class VQA:
    def __init__(self, question_file, annotation_file=None, test_mode=False):
        """Constructor of VQA helper class for reading and visualizing questions and answers.

        Args:
            question_file (str): location of VQA question file
            annotation_file (str, optional): location of VQA annotation file. Defaults to None.
            test_mode (bool, optional): set to True to avoid loading annotations. Defaults to False.
        """
        if not annotation_file:
            assert test_mode, 'No annotation file specified and test_mode is False'
        assert question_file is not None, 'Question file not specified'
        # load dataset
        self.dataset    = {}
        self.questions  = {}
        self.qa         = {}
        self.qqa        = {}
        self.imgToQA    = {}
        self.test_mode  = test_mode

        time_t = datetime.datetime.utcnow()
        if not self.test_mode:
            print('loading VQA annotations and questions into memory...')
            dataset = json.load(open(annotation_file, 'r'))
        else:
            print('test mode: loading only VQA questions into memory...')
            dataset = None
        questions       = json.load(open(question_file, 'r'))
        print(datetime.datetime.utcnow() - time_t)

        self.dataset    = dataset
        self.questions  = questions
        self.createIndex()


    def createIndex(self):
        # create index
        print('creating index...')
        if not self.test_mode:
            imgToQA = {ann['image_id']:     [] for ann in self.dataset['annotations']}
            qa      = {ann['question_id']:  [] for ann in self.dataset['annotations']}
            qqa     = {ann['question_id']:  [] for ann in self.dataset['annotations']}
            for ann in self.dataset['annotations']:
                imgToQA[ann['image_id']]    += [ann]
                qa[ann['question_id']]      = ann
            for ques in self.questions['questions']:
                qqa[ques['question_id']]    = ques

            print('index created!')
            # create class members
            self.qa = qa
            self.qqa = qqa
            self.imgToQA = imgToQA
        else:
            imgToQA = {ann['image_id']:     [] for ann in self.questions['questions']}
            qa      = {ann['question_id']:  [] for ann in self.questions['questions']}
            qqa     = {ann['question_id']:  [] for ann in self.questions['questions']}
            for quest in self.questions['questions']:
                imgToQA[quest['image_id']]  += [quest]
                qa[quest['question_id']]    = quest
            for quest in self.questions['questions']:
                qqa[quest['question_id']]   = quest

            print('index created!')
            # create class members
            self.qa = qa
            self.qqa = qqa
            self.imgToQA = imgToQA            


    def info(self):
        """Print information about the VQA annotation file.
        """
        info = self.dataset['info'] if self.test_mode else self.questions['info']
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
        if self.test_mode:
            raise NotImplementedError('Not available when test_mode=True')
        imgIds       = imgIds    if type(imgIds)    == list else [imgIds]
        quesTypes = quesTypes if type(quesTypes) == list else [quesTypes]
        ansTypes  = ansTypes  if type(ansTypes)  == list else [ansTypes]

        if len(imgIds) == len(quesTypes) == len(ansTypes) == 0:
            anns = self.dataset['annotations']
        else:
            if not len(imgIds) == 0:
                anns = sum([self.imgToQA[imgId] for imgId in imgIds if imgId in self.imgToQA],[])
            else:
                 anns = self.dataset['annotations']
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
        if self.test_mode:
            raise NotImplementedError('Not available when test_mode=True')
        quesIds   = quesIds   if type(quesIds)   == list else [quesIds]
        quesTypes = quesTypes if type(quesTypes) == list else [quesTypes]
        ansTypes  = ansTypes  if type(ansTypes)  == list else [ansTypes]

        if len(quesIds) == len(quesTypes) == len(ansTypes) == 0:
            anns = self.dataset['annotations']
        else:
            if not len(quesIds) == 0:
                anns = sum([self.qa[quesId] for quesId in quesIds if quesId in self.qa],[])
            else:
                anns = self.dataset['annotations']
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
        if self.test_mode:
            raise NotImplementedError('Not available when test_mode=True')
        if type(ids) == list:
            return [self.qa[id] for id in ids]
        elif type(ids) == int:
            return [self.qa[ids]]


    def showQA(self, anns):
        """Display the specified annotations.

        Args:
            anns (list): annotations to display

        Raises:
            NotImplementedError: [description]
        """
            
        if self.test_mode:
            raise NotImplementedError('Not available when test_mode=True')
        if len(anns) == 0:
            return 0
        for ann in anns:
            quesId = ann['question_id']
            print("Question: %s" %(self.qqa[quesId]['question']))
            for ans in ann['answers']:
                print("Answer %d: %s" %(ans['answer_id'], ans['answer']))


    def loadRes(self, resFile, quesFile):
        #todo implement when test_mode=True
        """Load result file and return a result object.

        Args:
            resFile (str): file name of result file
            quesFile (str): file name of question file

        Raises:
            NotImplementedError: [description]

        Returns:
            obj: result api object
        """
        if self.test_mode:
            raise NotImplementedError('Not available when test_mode=True')
        res = VQA()
        res.questions = json.load(open(quesFile))
        res.dataset['info'] = copy.deepcopy(self.questions['info'])
        res.dataset['task_type'] = copy.deepcopy(self.questions['task_type'])
        res.dataset['data_type'] = copy.deepcopy(self.questions['data_type'])
        res.dataset['data_subtype'] = copy.deepcopy(self.questions['data_subtype'])
        res.dataset['license'] = copy.deepcopy(self.questions['license'])

        print('Loading and preparing results...     ')
        time_t = datetime.datetime.utcnow()
        anns    = json.load(open(resFile))
        assert type(anns) == list, 'results is not an array of objects'
        annsQuesIds = [ann['question_id'] for ann in anns]
        assert set(annsQuesIds) == set(self.getQuesIds()), \
        'Results do not correspond to current VQA set. Either the results do not have predictions for all question ids in annotation file or there is atleast one question id that does not belong to the question ids in the annotation file.'
        for ann in anns:
            quesId                  = ann['question_id']
            if res.dataset['task_type'] == 'Multiple Choice':
                assert ann['answer'] in self.qqa[quesId]['multiple_choices'], 'predicted answer is not one of the multiple choices'
            qaAnn                = self.qa[quesId]
            ann['image_id']      = qaAnn['image_id']
            ann['question_type'] = qaAnn['question_type']
            ann['answer_type']   = qaAnn['answer_type']
        print('DONE (t=%0.2fs)'%((datetime.datetime.utcnow() - time_t).total_seconds()))

        res.dataset['annotations'] = anns
        res.createIndex()
        return res
