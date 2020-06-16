# coding: utf-8
import argparse
import os
import random

import matplotlib.pyplot as plt
import skimage.io as io

from VQAapi import VQA

#print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))



def demo(annFile, quesFile, imgDir, dataSubType):
    # initialize VQA api for QA annotations
    vqa=VQA(annFile, quesFile)

    # load and display QA annotations for given question types
    """
    All possible quesTypes for abstract and mscoco has been provided in respective text files in ../QuestionTypes/ folder.
    """
    annIds = vqa.getQuesIds(quesTypes='how many');
    anns = vqa.loadQA(annIds)
    randomAnn = random.choice(anns)
    vqa.showQA([randomAnn])
    imgId = randomAnn['image_id']
    imgFilename = 'COCO_' + dataSubType + '_'+ str(imgId).zfill(12) + '.jpg'
    if os.path.isfile(imgDir + imgFilename):
        I = io.imread(imgDir + imgFilename)
        plt.imshow(I)
        plt.axis('off')
        plt.show()

    # load and display QA annotations for given answer types
    """
    ansTypes can be one of the following
    yes/no
    number
    other
    """
    annIds = vqa.getQuesIds(ansTypes='yes/no');
    anns = vqa.loadQA(annIds)
    randomAnn = random.choice(anns)
    vqa.showQA([randomAnn])
    imgId = randomAnn['image_id']
    imgFilename = 'COCO_' + dataSubType + '_'+ str(imgId).zfill(12) + '.jpg'
    if os.path.isfile(imgDir + imgFilename):
        I = io.imread(imgDir + imgFilename)
        plt.imshow(I)
        plt.axis('off')
        plt.show()

    # load and display QA annotations for given images
    """
    Usage: vqa.getImgIds(quesIds=[], quesTypes=[], ansTypes=[])
    Above method can be used to retrieve imageIds for given question Ids or given question types or given answer types.
    """
    ids = vqa.getImgIds()
    annIds = vqa.getQuesIds(imgIds=random.sample(ids,5));
    anns = vqa.loadQA(annIds)
    randomAnn = random.choice(anns)
    vqa.showQA([randomAnn])
    imgId = randomAnn['image_id']
    imgFilename = 'COCO_' + dataSubType + '_'+ str(imgId).zfill(12) + '.jpg'
    if os.path.isfile(imgDir + imgFilename):
        I = io.imread(imgDir + imgFilename)
        plt.imshow(I)
        plt.axis('off')
        plt.show()




if __name__ == '__main__':
    """
    example usage:
        python -m tests.vqaDemo \
            --annFile ../__DATA__/VQA2.0/train/v2_mscoco_train2014_annotations.json \
            --quesFile ../__DATA__/VQA2.0/train/v2_OpenEnded_mscoco_train2014_questions.json \
            --imgDir ../__DATA__/VQA2.0/train/train2014 \
            --dataSubType train2014
    """

    parser = argparse.ArgumentParser()

    #read user parameters
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
    dataDir        ='../../VQA'
    versionType ='v2_' # this should be '' when using VQA v2.0 dataset
    taskType    ='OpenEnded' # 'OpenEnded' only for v2.0. 'OpenEnded' or 'MultipleChoice' for v1.0
    dataType    ='mscoco'  # 'mscoco' only for v1.0. 'mscoco' for real and 'abstract_v002' for abstract for v1.0.
    dataSubType ='train2014'
    annFile     ='%s/Annotations/%s%s_%s_annotations.json'%(dataDir, versionType, dataType, dataSubType)
    quesFile    ='%s/Questions/%s%s_%s_%s_questions.json'%(dataDir, versionType, taskType, dataType, dataSubType)
    imgDir         = '%s/Images/%s/%s/' %(dataDir, dataType, dataSubType)
    """
    demo(annFile=args.annFile, quesFile=args.quesFile, imgDir=args.imgDir, dataSubType=args.dataSubType)
