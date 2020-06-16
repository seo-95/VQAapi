# coding: utf-8

import sys
#dataDir = '../../VQA'
#sys.path.insert(0, '%s/PythonHelperTools/vqaTools' %(dataDir))
from VQAapi import VQA, VQAEval
import matplotlib.pyplot as plt
import skimage.io as io
import json
import random
import os
import argparse


if __name__ == '__main__':
    """
    example usage:
        python -m tests.vqaEvalDemo \
            --annFile ../__DATA__/VQA2.0/train/v2_mscoco_train2014_annotations.json \
            --quesFile ../__DATA__/VQA2.0/train/v2_OpenEnded_mscoco_train2014_questions.json \
            --imgDir ../__DATA__/VQA2.0/train/train2014 \
            --dataSubType train2014
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--annFile",
        type=str,
        required=True,
        help="Path to annotation file"
    )
    parser.add_argument(
        "--quesFile",
        type=str,
        required=True,
        help="Path to question file"
    )
    parser.add_argument(
        "--imgDir",
        type=str,
        required=True,
        help="Path to images folder"
    )
    parser.add_argument(
        "--dataSubType",
        type=str,
        required=True,
        help="One between 'train2014' or 'val2015'"
    )
    args = parser.parse_args()

    """
    # set up file names and paths
    versionType ='v2_' # this should be '' when using VQA v2.0 dataset
    taskType    ='OpenEnded' # 'OpenEnded' only for v2.0. 'OpenEnded' or 'MultipleChoice' for v1.0
    dataType    ='mscoco'  # 'mscoco' only for v1.0. 'mscoco' for real and 'abstract_v002' for abstract for v1.0.
    dataSubType ='train2014'
    annFile     ='%s/Annotations/%s%s_%s_annotations.json'%(dataDir, versionType, dataType, dataSubType)
    quesFile    ='%s/Questions/%s%s_%s_%s_questions.json'%(dataDir, versionType, taskType, dataType, dataSubType)
    imgDir      ='%s/Images/%s/%s/' %(dataDir, dataType, dataSubType)
    resultType  ='fake'
    fileTypes   = ['results', 'accuracy', 'evalQA', 'evalQuesType', 'evalAnsType']
    """
    versionType ='v1_' # this should be '' when using VQA v2.0 dataset --- THE FILE IS NOT IN THE CORRECT FORMAT
    resultType  ='fake'
    fileTypes   = ['results', 'accuracy', 'evalQA', 'evalQuesType', 'evalAnsType']
    taskType    ='OpenEnded' # 'OpenEnded' only for v2.0. 'OpenEnded' or 'MultipleChoice' for v1.0
    dataType    ='mscoco'  # 'mscoco' only for v1.0. 'mscoco' for real and 'abstract_v002' for abstract for v1.0.
    dataDir     = 'tests/'

    # An example result json file has been provided in './Results' folder.

    [resFile, accuracyFile, evalQAFile, evalQuesTypeFile, evalAnsTypeFile] = ['%s/Results/%s%s_%s_%s_%s_%s.json'%(dataDir, versionType, taskType, dataType, args.dataSubType, \
    resultType, fileType) for fileType in fileTypes]

    # create vqa object and vqaRes object
    vqa = VQA(args.annFile, args.quesFile)
    vqaRes = vqa.loadRes(resFile, args.quesFile)

    # create vqaEval object by taking vqa and vqaRes
    vqaEval = VQAEval(vqa, vqaRes, n=2)   #n is precision of accuracy (number of places after decimal), default is 2

    # evaluate results
    """
    If you have a list of question ids on which you would like to evaluate your results, pass it as a list to below function
    By default it uses all the question ids in annotation file
    """
    vqaEval.evaluate()

    # print accuracies
    print("\n")
    print("Overall Accuracy is: %.02f\n" %(vqaEval.accuracy['overall']))
    print("Per Question Type Accuracy is the following:")
    for quesType in vqaEval.accuracy['perQuestionType']:
        print ("%s : %.02f" %(quesType, vqaEval.accuracy['perQuestionType'][quesType]))
    print("\n")
    print("Per Answer Type Accuracy is the following:")
    for ansType in vqaEval.accuracy['perAnswerType']:
        print ("%s : %.02f" %(ansType, vqaEval.accuracy['perAnswerType'][ansType]))
    print("\n")
    # demo how to use evalQA to retrieve low score result
    evals = [quesId for quesId in vqaEval.evalQA if vqaEval.evalQA[quesId]<35]   #35 is per question percentage accuracy
    if len(evals) > 0:
        print('ground truth answers')
        randomEval = random.choice(evals)
        randomAnn = vqa.loadQA(randomEval)
        vqa.showQA(randomAnn)

        print('\n')
        print('generated answer (accuracy %.02f)'%(vqaEval.evalQA[randomEval]))
        ann = vqaRes.loadQA(randomEval)[0]
        print("Answer:   %s\n" %(ann['answer']))

        imgId = randomAnn[0]['image_id']
        imgFilename = 'COCO_' + args.dataSubType + '_'+ str(imgId).zfill(12) + '.jpg'
        if os.path.isfile(args.imgDir + imgFilename):
            I = io.imread(args.imgDir + imgFilename)
            plt.imshow(I)
            plt.axis('off')
            plt.show()

    # plot accuracy for various question types
    plt.bar(range(len(vqaEval.accuracy['perQuestionType'])), vqaEval.accuracy['perQuestionType'].values(), align='center')
    plt.xticks(range(len(vqaEval.accuracy['perQuestionType'])), vqaEval.accuracy['perQuestionType'].keys(), rotation='0',fontsize=10)
    plt.title('Per Question Type Accuracy', fontsize=10)
    plt.xlabel('Question Types', fontsize=10)
    plt.ylabel('Accuracy', fontsize=10)
    plt.show()

    # save evaluation results to ./Results folder
    json.dump(vqaEval.accuracy,     open(accuracyFile,     'w'))
    json.dump(vqaEval.evalQA,       open(evalQAFile,       'w'))
    json.dump(vqaEval.evalQuesType, open(evalQuesTypeFile, 'w'))
    json.dump(vqaEval.evalAnsType,  open(evalAnsTypeFile,  'w'))