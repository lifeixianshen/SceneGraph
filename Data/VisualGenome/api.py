from __future__ import print_function
import utils


def GetAllImageIds():
    """
    Get all Image ids.
    """
    page = 1
    next = f'/api/v0/images/all?page={page}'
    ids = []
    while True:
        data = utils.RetrieveData(next)
        ids.extend(data['results'])
        if data['next'] is None:
            break
        page += 1
        next = f'/api/v0/images/all?page={page}'
    return ids


def GetImageIdsInRange(startIndex=0, endIndex=99):
    """
    Get Image ids from startIndex to endIndex.
    """
    idsPerPage = 1000
    startPage = startIndex / idsPerPage + 1
    endPage = endIndex / idsPerPage + 1
    ids = []
    for page in range(startPage, endPage + 1):
        data = utils.RetrieveData(f'/api/v0/images/all?page={str(page)}')
        ids.extend(data['results'])
    ids = ids[startIndex % 100:]
    return ids[:endIndex - startIndex + 1]


def GetImageData(id=61512):
    """
    Get data about an image.
    """
    data = utils.RetrieveData(f'/api/v0/images/{str(id)}')
    if 'detail' in data and data['detail'] == 'Not found.':
        return None
    return utils.ParseImageData(data)


def GetRegionDescriptionsOfImage(id=61512):
    """
    Get the region descriptions of an image.
    """
    image = GetImageData(id=id)
    data = utils.RetrieveData(f'/api/v0/images/{str(id)}/regions')
    if 'detail' in data and data['detail'] == 'Not found.':
        return None
    return utils.ParseRegionDescriptions(data, image)


def GetRegionGraphOfRegion(image_id=61512, region_id=1):
    """
    Get Region Graph of a particular Region in an image.
    """
    image = GetImageData(id=image_id)
    data = utils.RetrieveData(
        f'/api/v0/images/{str(image_id)}/regions/{str(region_id)}'
    )
    if 'detail' in data and data['detail'] == 'Not found.':
        return None
    return utils.ParseGraph(data[0], image)


def GetSceneGraphOfImage(id=61512):
    """
    Get Scene Graph of an image.
    """
    image = GetImageData(id=id)
    data = utils.RetrieveData(f'/api/v0/images/{str(id)}/graph')
    if 'detail' in data and data['detail'] == 'Not found.':
        return None
    return utils.ParseGraph(data, image)


def GetAllQAs(qtotal=100):
    """
    Gets all the QA from the dataset.
    qtotal    int       total number of QAs to return. Set to None if all QAs should be returned
    """
    page = 1
    next = f'/api/v0/qa/all?page={page}'
    qas = []
    image_map = {}
    while True:
        data = utils.RetrieveData(next)
        for d in data['results']:
            if d['image'] not in image_map:
                image_map[d['image']] = GetImageData(id=d['image'])
        qas.extend(utils.ParseQA(data['results'], image_map))
        if qtotal is not None and len(qas) > qtotal:
            return qas
        if data['next'] is None:
            break
        page += 1
        next = f'/api/v0/qa/all?page={page}'
    return qas


def GetQAofType(qtype='why', qtotal=100):
    """
    Get all QA's of a particular type - example, 'why'
    qtype     string    possible values: what, where, when, why, who, how.
    qtotal    int       total number of QAs to return. Set to None if all QAs should be returned
    """
    page = 1
    next = f'/api/v0/qa/{qtype}?page={page}'
    qas = []
    image_map = {}
    while True:
        data = utils.RetrieveData(next)
        for d in data['results']:
            if d['image'] not in image_map:
                image_map[d['image']] = GetImageData(id=d['image'])
        qas.extend(utils.ParseQA(data['results'], image_map))
        if qtotal is not None and len(qas) > qtotal:
            return qas
        if data['next'] is None:
            break
        page += 1
        next = f'/api/v0/qa/{qtype}?page={page}'
    return qas


def GetQAofImage(id=61512):
    """
    Get all QAs for a particular image.
    """
    page = 1
    next = f'/api/v0/image/{str(id)}/qa?page={page}'
    qas = []
    image_map = {}
    while True:
        data = utils.RetrieveData(next)
        for d in data['results']:
            if d['image'] not in image_map:
                image_map[d['image']] = GetImageData(id=d['image'])
        qas.extend(utils.ParseQA(data['results'], image_map))
        if data['next'] is None:
            break
        page += 1
        next = f'/api/v0/image/{str(id)}/qa?page={page}'
    return qas

