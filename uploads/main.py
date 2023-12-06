import os
import sys
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import threshold_local
from PIL import Image
import pytesseract
import re
import joblib
import json
import warnings 
warnings.filterwarnings("ignore")


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def categorize_files(image_name):
    is_picture = True

    img = Image.open(image_name)

    # Check image dimensions
    width, height = img.size
    if 400 <= width <= 1200 and 700 <= height <= 1010:
        is_picture = True
    else:
        is_picture = False

    return is_picture


def opencv_resize(image, ratio):
    width = int(image.shape[1] * ratio)
    height = int(image.shape[0] * ratio)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)


def plot_rgb(image):
    plt.figure(figsize=(16, 10))
    return plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def plot_gray(image):
    plt.figure(figsize=(16, 10))
    return plt.imshow(image, cmap='Greys_r')


# approximate the contour by a more primitive polygon shape
def approximate_contour(contour, n: float = 0.032):
    peri = cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, n * peri, True)


# i need to loop the n numbers to find the best how.
def get_receipt_contour(contours):
    # loop over the contours
    for i, c in enumerate(contours):
        approx = approximate_contour(c, 0.032)
        # if our approximated contour has four points, we can assume it is receipt's rectangle
        if len(approx) == 4:
            return approx
    return None


def contour_to_rect(contour, resize_ratio: float):
    pts = contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    # top-left point has the smallest sum
    # bottom-right has the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # compute the difference between the points:
    # the top-right will have the minimum difference
    # the bottom-left will have the maximum difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect / resize_ratio


def wrap_perspective(img, rect):
    # unpack rectangle points: top left, top right, bottom right, bottom left
    (tl, tr, br, bl) = rect
    # compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    # compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    # take the maximum of the width and height values to reach
    # our final dimensions
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))
    # destination points which will be used to map the screen to a "scanned" view
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # calculate the perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    # warp the perspective to grab the screen
    return cv2.warpPerspective(img, M, (maxWidth, maxHeight))


def preprocess(file_name):
    image = cv2.imread(file_name)
    resize_ratio = 500 / image.shape[0]
    original = image.copy()
    image = opencv_resize(image, resize_ratio)

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 3: Blur
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Step 4: Dilate
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    dilated = cv2.dilate(blurred, rectKernel)

    # Step 5: Canny edge detector
    edges = cv2.Canny(dilated, 100, 200, apertureSize=3)

    # Step 6: Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Step 7: Get 10 largest contours
    largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    # Step 8: Get receipt contour
    receipt_contour = get_receipt_contour(largest_contours)

    # Step 9: Draw receipt contour
    image_with_receipt_contour = cv2.drawContours(image.copy(), [receipt_contour], -1, (0, 255, 0), 2)

    # Step 10: Convert contour to rectangle and warp perspective
    rect = contour_to_rect(receipt_contour, resize_ratio)
    scanned = wrap_perspective(original.copy(), rect)

    # Convert to image for saving
    image = Image.fromarray(scanned)

    return image


# Function to perform OCR
def perform_ocr(image):
    # Perform OCR
    ocr_result = pytesseract.image_to_string(image, config='--psm 6')

    return ocr_result


def process(image_name):
    is_picture = categorize_files(image_name)

    # Only preprocess picture files
    if is_picture:
        preprocessed = preprocess(image_name)
    else:
        preprocessed = Image.open(image_name)

    preprocessed.save(image_name)
    
    ocr_text = perform_ocr(preprocessed)
    # Convert OCR text to lowercase
    ocr_text_lower = ocr_text.lower()

    return ocr_text_lower


def check_currency_conditions(text):
    # Define the regular expression pattern for matching currency conditions
    currency_pattern = re.compile(r'\b(\d+\.\d+|\d+)\s*([$]|chf)\b', re.IGNORECASE | re.UNICODE)

    # Check if the currency conditions are met
    return bool(currency_pattern.search(text))


def process_text(text):
    # Load the pre-trained model
    loaded_model = joblib.load('NB200.joblib')  # Replace with the actual filename

    # Check currency conditions
    if not check_currency_conditions(text):
        sentences = ['Description', 'xxxxxxxxx li hua hotel inv room', 'xxxxxxxxx li hua hotel inv ref',
                     'xxxxxxxxx li hua hotel robinson bennet', 'kama labuan base visit hotel mariner hotel labuan inv',
                     'muhd shafiq hotel labuan point', 'shahidan ramli labuan hotel',
                     'muzaffar hotel red hotel kuantan', 'zulkipli accommodation mehram hotel inv',
                     'agoda hotel mohammad xxxxxxxxxt royale chulan', 'royale chulan hotel mohamad xxxxxxxxxt',
                     'xxxxxxxxx rxxxxxxxxx accomadation seaview timurbay rcpt',
                     'xxxxxxxxx rxxxxxxxxx accomodation seaview timurbay rcpt', 'xxxxxxxxx farhaan accom',
                     'xxxxxxxxx farhaan accomodation klsuites services soho',
                     'xxxxxxxxx hilmy hotel sri melaysia penang site visit bukit selambau inv htin',
                     'shahidan ramli home hotel', 'century inn accomodation andreas rizky',
                     'century inn accomodation nurul xxxxxxxxx rosli', 'xxxxxxxxx othman hotel',
                     'xxxxxxxxx thistle johor baharu agoda', 'nur iza accommodation brow hotel penang',
                     'xxxxxxxxx alfeizal hotel thistle johor bharu inv',
                     'xxxxxxxxx alfeizal riverbank hotel inv meeting nafas tesdec du',
                     'xxxxxxxxx xxxxxxxxx hotel dorsett', 'nur fatihah marjan hotel inv',
                     'xxxxxxxxx nursyafiq hotel patuh tegur pcsb', 'ad staff travel local accomodation',
                     'golden uptrend hotel charge mohamad ismat', 'sayu travel hotel ahmad ridhuan',
                     'sayu travel hotel nurul amirah', 'sayu travel hotel charge well solutions staff',
                     'xxxxxxxxx surabaya hotel inv', 'xxxxxxxxx kamarul movenpick varan hotel ankara turkiye trip',
                     'zaleha radission blu hotel london inv', 'zaleha tower suites blue orchid inv',
                     'xxxxxxxxx arifin sultan hotel residence lounge jakarta idr',
                     'uzma intern allowance gspd ws temana', 'lng staff salary telco',
                     'lng staff salary transportation', 'prepayment misc charge dependent education dkrm sara ghazi',
                     'sk payroll closing rea', 'sk payroll closing telco', 'sk payroll closing trans',
                     'staff salary director fee acting allowance admin', 'staff salary director fee trans legal',
                     'staff salary director fee accomodation qhse',
                     'staff salary director fee acting allowance ceo office', 'staff salary director fee telco admin',
                     'staff salary director fee telco ceo office', 'staff salary director fee telco communication',
                     'staff salary director fee telco finance', 'staff salary director fee telco gscm cc cm',
                     'staff salary director fee telco erp', 'staff salary director fee telco legal',
                     'staff salary director fee telco people', 'staff salary director fee telco qhse',
                     'staff salary director fee telco scm', 'staff salary director fee telcobp gscm cc cm',
                     'staff salary director fee telcobp qhse', 'staff salary director fee trans admin',
                     'staff salary director fee trans ceo office', 'staff salary director fee trans communication',
                     'staff salary director fee trans finance', 'staff salary director fee trans gscm cc cm',
                     'staff salary director fee trans erp', 'staff salary director fee trans people',
                     'staff salary director fee trans qhse', 'staff salary director fee trans scm',
                     'staff salary director fee transbp gscm cc cm', 'staff salary director fee transbp qhse',
                     'staff salary acting allowance', 'staff salary telco', 'staff salary transportation',
                     'ual staff salary telco', 'ual staff salary trans',
                     'uesb staff salary bg bd strategy sales telco allow',
                     'uesb staff salary bg bd strategy sales trans allow',
                     'uesb staff salary bg laboratory telco allow', 'uesb staff salary bg laboratory trans allow',
                     'uesb staff salary business growth telco allow', 'uesb staff salary business growth trans allow',
                     'uesb staff salary group operation readiness assurance telco allow',
                     'uesb staff salary gws drilling agency allow', 'uesb staff salary gws drilling agency telco allow',
                     'uesb staff salary gws drilling agency trans allow',
                     'uesb staff salary gora base yard operation telco allow',
                     'uesb staff salary gora base yard operation trans allow', 'uesb staff salary gpsd lps telco allow',
                     'uesb staff salary gpsd lps trans allow',
                     'uesb staff salary gpsd water solutions pwim sepat telco allow',
                     'uesb staff salary gpsd water solutions pwim sepat trans allow',
                     'uesb staff salary gpsd water solutions pwim temana telco allow',
                     'uesb staff salary gpsd water solutions pwim temana trans allow',
                     'uesb staff salary gpsd water solutions wim tax allow',
                     'uesb staff salary gpsd water solutions wim tax allow cp',
                     'uesb staff salary gpsd water solutions wim telco allow',
                     'uesb staff salary gpsd water solutions wim trans allow',
                     'uesb staff salary gpsd welltest filtration bp telco allow',
                     'uesb staff salary gpsd welltest filtration bp trans allow',
                     'uesb staff salary group operation readiness assurance trans allow',
                     'uesb staff salary gws integrated project management offshore allowance',
                     'uesb staff salary gws integrated project management telco allow',
                     'uesb staff salary gws integrated project management trans allow',
                     'uesb staff salary gws wireline telco allow', 'uesb staff salary gws wireline trans allow',
                     'uzma intern allowance', 'uzma intern allowance gspd ws temana', 'lng staff salary telco',
                     'lng staff salary transportation', 'prepayment misc charge dependent education dkrm sara ghazi',
                     'reversal prepayment misc detik harapan tuition fee sara kamarul redzuan year',
                     'reversal prepayment detik harapan tuition fee ghazi kamarul redzuan year',
                     'reversal prepayment dkrm scholarship award ms uzma', 'sk payroll closing telco',
                     'sk payroll closing trans', 'staff salary director fee telco ceo office',
                     'staff salary director fee telco legal', 'staff salary director fee telco people',
                     'staff salary director fee trans ceo office', 'staff salary director fee accomodation qhse',
                     'staff salary director fee acting allowance admin',
                     'staff salary director fee acting allowance ceo office',
                     'staff salary director fee offshore allowance qhse', 'staff salary director fee telco admin',
                     'staff salary director fee telco communication', 'staff salary director fee telco finance',
                     'staff salary director fee telco gscm cc cm', 'staff salary director fee telco erp',
                     'staff salary director fee telco qhse', 'staff salary director fee telco scm',
                     'staff salary director fee trans admin', 'staff salary director fee trans communication',
                     'staff salary director fee trans finance', 'staff salary director fee trans gscm cc cm',
                     'staff salary director fee trans erp', 'staff salary director fee trans legal',
                     'staff salary director fee trans people', 'staff salary director fee trans qhse',
                     'staff salary director fee trans scm', 'staff salary acting allowance', 'staff salary telco',
                     'staff salary transportation', 'ual staff salary telco', 'ual staff salary trans',
                     'uesb staff salary bg bd strategy sales telco allow',
                     'uesb staff salary bg bd strategy sales trans allow',
                     'uesb staff salary bg laboratory telco allow', 'uesb staff salary bg laboratory trans allow',
                     'uesb staff salary business growth telco allow', 'uesb staff salary business growth trans allow',
                     'uesb staff salary gora base yard operation telco allow',
                     'uesb staff salary gora base yard operation trans allow', 'uesb staff salary gpsd lps telco allow',
                     'uesb staff salary gpsd lps trans allow',
                     'uesb staff salary gpsd water solutions pwim sepat telco allow',
                     'uesb staff salary gpsd water solutions pwim sepat trans allow',
                     'uesb staff salary gpsd water solutions pwim temana telco allow',
                     'uesb staff salary gpsd water solutions pwim temana trans allow',
                     'uesb staff salary gpsd water solutions wim tax allow',
                     'uesb staff salary gpsd water solutions wim tax allow cp',
                     'uesb staff salary gpsd water solutions wim telco allow',
                     'uesb staff salary gpsd water solutions wim trans allow',
                     'uesb staff salary gpsd welltest filtration bp telco allow',
                     'uesb staff salary gpsd welltest filtration bp trans allow',
                     'uesb staff salary group operation readiness assurance telco allow',
                     'uesb staff salary group operation readiness assurance trans allow',
                     'uesb staff salary gws drilling agency allow', 'uesb staff salary gws drilling agency telco allow',
                     'uesb staff salary gws drilling agency trans allow',
                     'uesb staff salary gws integrated project management telco allow',
                     'uesb staff salary gws integrated project management trans allow',
                     'uesb staff salary gws wireline telco allow', 'uesb staff salary gws wireline trans allow',
                     'uzma intern allowance', 'bank charges scb usd', 'bank charges fund transfer uesb –',
                     'bank charges month giro', 'bank charges abb', 'bank charges amb', 'bank charges amb',
                     'bank charges amb', 'bank charges amb', 'bank charges hsbc', 'bank charges rhb',
                     'bank charges rhb', 'bank charges scb', 'bank charges scb', 'bank charges rhb myr', 'hsbc charges',
                     'prepayment misc bg ibg', 'rhb audit confirmation non borrowing account',
                     'rhb audit confirmation non borrowing account', 'rhb bank charges subscription chgs',
                     'uesb prepayment bank guarantee pwim', 'uesb prepayment bank guarantee rhb bg comm tcxg kup pcsb',
                     'uesb prepayment charges apnkli pcsb',
                     'uesb prepayment gte issue comm charges lejkli gtrf tk pengarah kastam',
                     'uesb prepayment bg comm pcsb tcxg jx nippon', 'uesb prepayment bg extension ksb ibg',
                     'uesb prepayment charges apnkli bg pcsb', 'uesb prepayment charges bg pttep sabah apnkli',
                     'uesb prepayment gte issue comm charges aapkli',
                     'uesb prepayment gte issue comm charges apnkli altus intervention',
                     'uesb prepayment gte issue comm charges apnkli altus intervention',
                     'uesb prepayment ambank petronas carigali sdn bhd flx', 'uesb prepayment ambank flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx', 'uesb prepayment financing flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx usd exchange rate',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx', 'uesb prepayment financing flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx', 'uesb prepayment financing flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx', 'uesb prepayment financing flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx rollover flx',
                     'uesb prepayment flx charges', 'uesb prepayment rhb bg comm tcxg kup cargolift',
                     'uesb prepayment scb bg charges', 'rhb rc cmrc rm mil due', 'lp bg scb petronas carigali',
                     'bg apnkli charges pttep sabah hwu', 'reclass pob bank charges commitment fee bursa fee',
                     'reclass pob bank charges commitment fee bursa fee',
                     'reclass pob bank charges commitment fee bursa fee', 'bank charges commitment fee',
                     'ambank dormant account fee', 'bank charges fund transfer uesb –', 'bank charges abb',
                     'bank charges amb', 'bank charges amb', 'bank charges amb', 'bank charges amb', 'bank charges amb',
                     'bank charges hsbc', 'bank charges rhb', 'bank charges rhb', 'bank charges scb',
                     'bank charges scb', 'bank charges rhb myr', 'hsbc charges biekli biekli biekli',
                     'hsbc charges biekli', 'hsbc charges biekli biekli', 'hsbc charges biekli',
                     'prepayment misc bg ibg', 'rhb bank charges', 'rhb reflex subscription charge',
                     'uesb prepayment misc bank guarantee pwim', 'uesb prepayment misc bg rhb bg comm tcxg kup pcsb',
                     'uesb prepayment misc lp bg scb petronas carigali',
                     'uesb prepayment misc bg apnkli charges pttep sabah hwu',
                     'uesb prepayment misc bg comm pcsb tcxg jx nippon', 'uesb prepayment misc bg extension ksb ibg',
                     'uesb prepayment misc bg pwim pcsb tcxg extention',
                     'uesb prepayment misc bg wireline pcsb tcxg kup', 'uesb prepayment misc charges apnkli pcsb',
                     'uesb prepayment misc charges bg pttep sabah apnkli bg extension',
                     'uesb prepayment misc gte issue comm charges aapkli',
                     'uesb prepayment misc gte issue comm charges apnkli altus intervention',
                     'uesb prepayment misc gte issue comm charges lejkli gtrf tk pengarah kastam',
                     'uesb prepayment misc gte issue comm charges apnkli altus intervention',
                     'uesb prepayment misc flx usd exchange rate',
                     'uesb prepayment misc ambank petronas carigali sdn bhd flx', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc ambank flx', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc ambank flx', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc ambank flx', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc ambank flx', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc ambank flx usd', 'uesb prepayment misc ambank flx',
                     'uesb prepayment misc financing flx', 'uesb prepayment misc financing flx',
                     'uesb prepayment misc financing flx', 'uesb prepayment misc financing flx',
                     'uesb prepayment misc financing flx', 'uesb prepayment misc financing flx',
                     'uesb prepayment misc financing flx', 'uesb prepayment misc financing flx',
                     'uesb prepayment misc financing flx', 'uesb prepayment misc financing flx rollover flx',
                     'uesb prepayment misc flx charges', 'uesb prepayment misc rhb bg comm tcxg kup cargolift',
                     'uesb prepayment misc scb bg charges', 'uesb prepayment charges apnkli bg pcsb',
                     'uesb prepayment charges bg pttep sabah apnkli', 'uesb prepayment financing flx',
                     'uesb prepayment financing flx', 'uesb prepayment financing flx', 'uesb prepayment financing flx',
                     'maziah printing notification shareholders th agm cs', 'notice annual general meeting',
                     'advertisement agm notice', 'dr therefore agm rehearsal',
                     'boardroom secretarial fees charges ub thirteenth agm', 'copywriting services annual report uzma',
                     'zeenatu document delivery bakti suci holdings', 'nationwide express courier chrg',
                     'nationwide express courier chrg', 'nationwide express courier chrg',
                     'nationwide express courier chrg', 'noblehouse courier charges', 'postages courier',
                     'nationwide express courier chrg', 'world asia cn tally soa',
                     'city link express courier original receipt inv plbu',
                     'aisya courier fee pos laju send letters bksa kum cs', 'courier brunei rizqma energy inv',
                     'grab express tengku ezuan inv dbgfwwjhc', 'lalamove delivery common seal inv',
                     'lalamove delivery board directors inv', 'lalamove delivery board directors invc',
                     'lalamove delivery boardmailer inv', 'lalamove delivery boardroom inv',
                     'lalamove delivery wm cosec inv', 'delivery assignment earnings messrs reed smith dhl',
                     'courier lbu kul repair return dts box bas', 'courier sin lbu pouzens air regulator assy',
                     'delivery charges labuan', 'courier charges', 'courier pouzens us ksb',
                     'escort fee due height cargo', 'gapima logistic charges wireline', 'custom duty labuan ksb',
                     'sales tax', 'transworldmark chraged custom duty sst', 'apm nuclear delivery cost',
                     'trucking singapore ksb incl permit', 'xxxxxxxxx client engagement coffee bean',
                     'xxxxxxxxx client engagement parathai klcc', 'ahmad yunus white sand simon ihlas',
                     'xxxxxxxxx demo cafe klcc meetg redang resort manager solar',
                     'xxxxxxxxx doemcafe klcc meetg solar selco prj itcc sabah',
                     'xxxxxxxxx nuin kafe bdr bangi meeting tmm psb solar grid',
                     'xxxxxxxxx park view cafe klcc meetg gopeng chd ceo vppa',
                     'xxxxxxxxx park view cafe klcc hj xxxxxxxxxil poultry wem',
                     'xxxxxxxxx seri pacific kl meetg chairman npk fertilizer',
                     'xxxxxxxxx restaurant bq discussion mbsb lss',
                     'xxxxxxxxx alfeizal meeting bakti suci white sand cafe',
                     'xxxxxxxxx alfeizal meeting project dome cafe',
                     'xxxxxxxxx alfeizal meeting strategic partner lng solar business inv tao',
                     'xxxxxxxxx alfeizal session ceo seda bakti suci caffe rc',
                     'xxxxxxxxx alfeizal session ceo seda bakti suci golf resort villa golf',
                     'sazlida enquest meeting dome cafe', 'sazlida enquest meeting rama',
                     'sazlida pttep meeting urban soul', 'sazlida seah meeting white sand',
                     'badminton court rent event client', 'warung mishary refreshment client pcsb',
                     'xxxxxxxxx nursyafiq client entertainment cafe exxon',
                     'xxxxxxxxx nursyafiq client entertainment dolly dim sum exxon',
                     'xxxxxxxxx nursyafiq client entertainment genki sushi exxon',
                     'xxxxxxxxx nursyafiq client entertainment parathai exxon',
                     'xxxxxxxxx nursyafiq client entertainment serai exxon',
                     'xxxxxxxxx nursyafiq client entertainment serai exxon',
                     'xxxxxxxxx nursyafiq client entertainment starbucks sb exxon',
                     'xxxxxxxxx nursyafiq client entertainment starbucks sb exxon',
                     'xxxxxxxxx nursyafiq client entertainment coffe bean exxon',
                     'xxxxxxxxx nursyafiq client entertainment coffee bean exxon',
                     'xxxxxxxxx nursyafiq client entertainment traders hotel exxon',
                     'xxxxxxxxx rxxxxxxxxx client entertainment pcsb restoren seri hijrah',
                     'xxxxxxxxx rxxxxxxxxx client entertainmnet foe pcsb kb brewster',
                     'xxxxxxxxx rxxxxxxxxx client entertainmnet foe pcsb restoran tong juan kemaman',
                     'xxxxxxxxx farhaan golg client kgpr', 'xxxxxxxxx farhaan meeting client wester mpm',
                     'xxxxxxxxx farhaan meeting client mpm starbuck', 'whitesand coffee nui lawyer inv',
                     'lunch inspection dosh kedai kopi kemaman hqp', 'xxxxxxxxx othman dinner auditor team',
                     'xxxxxxxxx othman dinner auditor team', 'xxxxxxxxx othman lunch auditor team',
                     'xxxxxxxxx kamarul bilgi fisi group dinner tubitak ankara turkiye trip inv',
                     'xxxxxxxxx kamarul jp teres lunch public investment bank inv',
                     'xxxxxxxxx kamarul nippori lunch geospatial team inv',
                     'xxxxxxxxx kamarul lankan crabs lunch deleum inv',
                     'xxxxxxxxx kamarul white sand bd discussion inv',
                     'xxxxxxxxx bape cafe klcc klcc meetg petronas ev changer',
                     'xxxxxxxxx ehsan bukit jelutong discussion kpj solar rooftoop',
                     'xxxxxxxxx lacrista hotel melaka meetg tnb research ceo smart',
                     'xxxxxxxxx onde onde makanery sb meeting blueleaf vppa',
                     'xxxxxxxxx sdish room meeting gopeng bhd vppa',
                     'xxxxxxxxx starbucks coffee sb meeting mimos team halal',
                     'xxxxxxxxx starbucks coffee sb meeting mimos team halal',
                     'xxxxxxxxx starbucks coffee sb meeting sime drby lss vppa lan',
                     'xxxxxxxxx thistle johor bahru discussion kejora nafas vppa sola',
                     'xxxxxxxxx white sand cafe discussion pkeinpk solar',
                     'xxxxxxxxx zara barn tahi putrajaya zbti meeting pkeinpk solar',
                     'xxxxxxxxx onde onde restaurant discussion tnb ceo vppa equ',
                     'ikhlas breakfast mais team new venture bakti suci inv chk',
                     'ikhlas golf booking mais new venture bakti suci inv gr',
                     'xxxxxxxxx alfeizal lunch ceo bina daruliman berhad bdb chili',
                     'xxxxxxxxx alfeizal dinner discussion ingress de wan',
                     'xxxxxxxxx alfeizal golf chairman mai selangor golf balls inv mig',
                     'xxxxxxxxx alfeizal golf chairman mai selangor lunch tanah na',
                     'zaleha meeting maybank huckleberry', 'xxxxxxxxx xxxxxxxxx entertaiment client dorsett',
                     'xxxxxxxxx xxxxxxxxx lunch client mandarin oriental klcc',
                     'xxxxxxxxx xxxxxxxxx lunch client samba brazillian steakhouse',
                     'xxxxxxxxx arifin autogrill soekarno airport idr',
                     'xxxxxxxxx arifin avenue bistro empire damansara inv', 'xxxxxxxxx arifin café klcc coffee pcs oga',
                     'xxxxxxxxx arifin chinoz park bangsar lunch mfm', 'xxxxxxxxx arifin dome cafe klcc coffee pcs',
                     'xxxxxxxxx arifin dotty klcc fast dewanto enquest cs',
                     'xxxxxxxxx arifin kenny hills baker ttdi breakfast seah ptusb',
                     'xxxxxxxxx arifin marini grand café klcc coffee pcs',
                     'xxxxxxxxx arifin marini grand cafe klcc lunch pcbs',
                     'xxxxxxxxx arifin metro senayan mall plaza senayan idr',
                     'xxxxxxxxx arifin nz curry house wangsa maju lunch pcsb baram',
                     'xxxxxxxxx arifin paul plaza senayan idr',
                     'xxxxxxxxx arifin restaurant sederhana matraman jakarta timur idr',
                     'xxxxxxxxx arifin wendy jakarta',
                     'xxxxxxxxx arifin white sand café empire damansara lunch petronas swift team',
                     'xxxxxxxxx arifin white sand café empire damansara', 'sazlida enquest meeting marini',
                     'sazlida petronas meeting starbuck sbr', 'sazlida pttep meeting urban soul sb',
                     'xxxxxxxxx nursyafiq client entertainment exxon', 'xxxxxxxxx nursyafiq client entertainment exxon',
                     'xxxxxxxxx farhaan badminton session pcsb cs',
                     'xxxxxxxxx farhaan badminton session pcsb shuttle cs',
                     'xxxxxxxxx farhaan lunch pax post ops meeting pcsb',
                     'xxxxxxxxx farhaan trophy pss volleyball tournament inv iv',
                     'gets mgmt renewal work permit jose lujan',
                     'gets mgmt payment cancellation employment pass hulsbos robert eise',
                     'gets mgmt application employment pass dependent pass christoper anthon',
                     'gets mgmt application employment pass dependent pass mochamad taufik',
                     'agensi pekerjaan castle work permit inv', 'agensi pekerjaan castle work permit inv',
                     'application employment pass hulsbos robert eise expired',
                     'application employment pass hulsbos robert eise spouse expired',
                     'castle handling fee sarawak employment pass mths rosfarnanie roslan',
                     'castle work permit months ideris alias', 'castle work permit mths zamlie', 'china visa',
                     'claim passport', 'nurul janna fuel wb', 'muhamad amir velfire fuel', 'caltex fuel company car',
                     'kemaman filing station fuel company car', 'petronas fuel company car bd fee',
                     'dht shell station base use transportation car company still mainte',
                     'dht shell station fuel using forklift inv', 'dht shell station fuel using forklift inv',
                     'petronas smartpay fuel charge wpt', 'petronas smartpay fuel charge wpt',
                     'petronas smartpay fuel charge wpt', 'petronas smartpay fuel charge wpt',
                     'petronas smartpay fuel charge wpt', 'petronas smartpay fuel charge wpt',
                     'petronas smartpay fuel charge wpt', 'petrol vab', 'xxxxxxxxx hilmy petrol co car',
                     'petronas smartpay fuel charge', 'dht shell station fuel using forklift inv',
                     'dht shell station fuel using forklift inv',
                     'petronas primax petronas base use transportation car company still',
                     'xxxxxxxxx xxxxxxxxx fuel refill', 'xxxxxxxxx xxxxxxxxx refill fuel petronas',
                     'accruals petronas smartpay', 'marsya xxxxxxxxx kamarul redzuan',
                     'prepayment misc charge get living london limited pob uesb ub pymt',
                     'prepayment misc charge lulu money malaysia sdn bhd pob uesb ub pymt',
                     'reversal prepayment pob uzma pymn living allowance scholarship award', 'gift mother day flowers',
                     'gift raya biscuits doc nurses neurosurgery', 'gift raya biscuits doc nurses ward',
                     'gift raya biscuits doc nurses ward', 'gift mosti', 'gift privasat', 'gifts client existing',
                     'machines lecture gift utp', 'meko bamboo toothbrush corporate gift agm',
                     'mst golf sponsorship spe terengganu polo shirt pulai',
                     'spe sponsorship spe terengganu golf pulai classic rm per flig', 'sponsorship utp convocation',
                     'sponsorship apgce geohack sponsorship', 'utp adjunct lecture gift',
                     'utp sponsorship award convocation', 'hrdf contribution salary communication',
                     'hrdf contribution salary ceo', 'hrdf contribution salary admin', 'hrdf contribution salary fin',
                     'hrdf contribution salary gscm', 'hrdf contribution salary gscm cc', 'hrdf contribution salary',
                     'hrdf contribution salary legal', 'hrdf contribution salary people',
                     'hrdf contribution salary qhse', 'uesb staff salary bg bd strategy sales hrdf',
                     'uesb staff salary bg laboratory hrdf', 'uesb staff salary business growth hrdf',
                     'uesb staff salary gws drilling agency hrdf', 'uesb staff salary gora base yard operations hrdf',
                     'uesb staff salary gora mrc hrdf', 'uesb staff salary gpsd lps hrdf',
                     'uesb staff salary gpsd water solutions pwim sepat hrdf',
                     'uesb staff salary gpsd water solutions pwim temana hrdf',
                     'uesb staff salary gpsd water solutions wim hrdf',
                     'uesb staff salary gpsd welltest filtration hrdf',
                     'uesb staff salary group operation readiness assurances hrdf',
                     'uesb staff salary gws integrated project management hrdf', 'uesb staff salary gws wireline hrdf',
                     'uesb staff salary bg bd strategy sales hrdf', 'uesb staff salary bg laboratory hrdf',
                     'uesb staff salary business growth hrdf', 'uesb staff salary gora base yard operations hrdf',
                     'uesb staff salary gora mrc hrdf', 'uesb staff salary gpsd lps hrdf',
                     'uesb staff salary gpsd water solutions pwim sepat hrdf',
                     'uesb staff salary gpsd water solutions pwim temana hrdf',
                     'uesb staff salary gpsd water solutions wim hrdf',
                     'uesb staff salary gpsd welltest filtration hrdf',
                     'uesb staff salary group operation readiness assurances hrdf',
                     'uesb staff salary gws drilling agency hrdf',
                     'uesb staff salary gws integrated project management hrdf', 'uesb staff salary gws wireline hrdf',
                     'mr diy tools cleaning', 'dell genuine latitude whr cell battery',
                     'hdmi replacement cable barco wireless display system',
                     'matte lcd wxga wide hd connector pin jvyc', 'bbln dell primary cell hr battery ky',
                     'apple com charger en asrul', 'apple com magic trackpad mac en asrul',
                     'apple com powe adapter en asrul', 'canon cart yellow toner', 'kingston gb sata ssd',
                     'muhazam mm mm converter ikano inv', 'muhazam micro hdmi hdmi cable ikano inv',
                     'muhazam max ninety nine extension socket tape ap',
                     'muhazam pc image electronic hdmi cable wangsa', 'office unit prorated charges st th',
                     'office proplus unit prorated charges st th',
                     'big dataworks ingress technologies ingress precision data',
                     'big dataworks uzma kuala muda mycrs certificate mida gita application inv',
                     'xxxxxxxxx aziz domain name renewal uzma paid',
                     'crowe registration income tax file number inland revenue board',
                     'xxxxxxxxx amilya pymn perolehan mof cert renewal register',
                     'lesen awam penjanaan tenaga boleh baharu suruhanjaya tenaga',
                     'uesb prepayment aelb license renewal yr lembaga perlesenan tenaga atom',
                     'uesb prepayment mbpj renewal signboard uesb license', 'bakti suci company profile bdsb',
                     'bakti suci solutions company profile bdsb', 'company profile elorist enterprise bdsb',
                     'company profile svp well services bdsb', 'geospatial ai company profile bdsb',
                     'kumpulan ladang terengganu profile bdsb', 'suria infiniti company profile bdsb',
                     'tdm berhad company profile en mazli directorate bdsb', 'transocean drilling company profile bdsb',
                     'uzma environergy company profile bdsb', 'uzma environergy form bdsb',
                     'uzma kuala muda company profile bdsb', 'uzma nexus company profile bdsb',
                     'uzma solar company profile bdsb',
                     'xxxxxxxxx amilya payment perolehan mof cert renewal certificate',
                     'lesen awam penjanaan tenaga boleh baharu suruhanjaya tenaga', 'petty cash kl expenses uzma apn',
                     'uesb prepayment misc aelb license renewal yr lembaga perlesenan tenaga atom',
                     'uesb prepayment misc mbpj renewal signboard uesb license',
                     'uesb prepayment misc software license annual renewal fardux',
                     'xxxxxxxxx borneo medical robinson rtk antigen inv',
                     'xxxxxxxxx kpj miri bennet tan rtk antigien inv', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing env',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'klinik alamanda medical exxon abdul hakim', 'klinik alamanda medical offshore exxon azhar',
                     'klinik alamanda medical offshore exxon suhardi', 'xxxxxxxxx norsyukry rtk ag klinik slam',
                     'xxxxxxxxx norsyukry rtk ag klinik primer',
                     'klinik syed offshore medical chek xxxxxxxxx nazirul faiz abdullah',
                     'pre medical check adha alia rusdey dhiya', 'pre medical check nur al amin muhd imran rosli',
                     'pre medical check nur azima fatima haziq sofrina zawanah', 'pre medical check shasha nur amanina',
                     'pre medical check shiya ayuni bt arifin', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing env',
                     'aia aso aso claim excess billing', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'aia aso aso claim excess billing uesb',
                     'aia aso aso claim excess billing uesb', 'reclass medical expenses depreciation pob',
                     'reclass medical expenses pob uzma apn',
                     'uesb staff salary gws integrated project management repay co aso',
                     'aqilah aziz fitness monthly reimbursable inv', 'lifelong prosperity saasgcc club membership dkrm',
                     'lifelong prosperity saasgcc club membership dkrm',
                     'prepayment misc charge term golf membership tpc', 'malaysian industry membership annual fee',
                     'aqilah aziz fitness monthly reimbursable inv', 'lifelong prosperity saasgcc club membership dkrm',
                     'prepayment misc charge term golf membership tpc',
                     'reversal prepayment linkedln job slots billing period',
                     'reversal prepayment linkedln recruiter corporate', 'xxxxxxxxx mileage zam buy consumble parts',
                     'xxxxxxxxx mileage kl home klia km',
                     'xxxxxxxxx aziz mileage ut svp ut km way tape relocation tape',
                     'xxxxxxxxx aziz mileage ut svp ut km way tape relocation tape',
                     'xxxxxxxxx aziz mileage ut svp ut km way tape relocation tape',
                     'xxxxxxxxx haziq mileage travel mitc business presentation penal',
                     'xxxxxxxxx haziq return mitc km', 'muzaffar mileage red hotel kuantan kop kerteh km',
                     'muzaffar mileage ut kuantan km', 'muzaffar mileage kuantan kl home km',
                     'xxxxxxxxxza hess btgb mileage', 'xxxxxxxxxza hess btgb mileage km',
                     'xxxxxxxxxza pcsb kacak mileage km', 'xxxxxxxxxza pttep mileage km',
                     'xxxxxxxxxza pttep sirung mileage km', 'zulkipli mileage kl kemaman kl km',
                     'xxxxxxxxx rosli mileage exxon office uzma km', 'xxxxxxxxx rosli mileage uzma exxon office km',
                     'xxxxxxxxxt jamali mileage kemaman kl km', 'xxxxxxxxxt jamali mileage kemaman kl km',
                     'xxxxxxxxx rxxxxxxxxx mileage kemaman home km', 'xxxxxxxxx rxxxxxxxxx mileage kemaman home km',
                     'xxxxxxxxx rxxxxxxxxx mileage home kemaman km',
                     'xxxxxxxxx rxxxxxxxxx xxxxxxxxx rxxxxxxxxx mileage home kemaman km',
                     'xxxxxxxxx farhaan mileage mkn kl workshop tag petronas event km',
                     'xxxxxxxxx farhaan mileage kl kmn workshop tag petronas event km',
                     'xxxxxxxxx norsyukry mileage home klinik salam grand putri hotel km',
                     'xxxxxxxxx norsyukry mileage suite hotel home km', 'shahidan ramli mileage rm km',
                     'xxxxxxxxx othman mileage home klia km', 'xxxxxxxxx othman mileage home klia km',
                     'xxxxxxxxx othman mileage home klia km', 'xxxxxxxxx othman mileage home klia km',
                     'xxxxxxxxx othman mileage hotel ksb hotel km', 'xxxxxxxxx othman mileage hotel ksb hotel km',
                     'xxxxxxxxx othman mileage kl kemaman kl km', 'xxxxxxxxx othman mileage home klia km',
                     'nur iza perbadanan air pinang sive visit mileage km',
                     'adham razali mileage ksb msts cherating ksb km way',
                     'adham razali mileage ksb msts cherating ksb way',
                     'azhar bin mohamad shahrin mileage ksb msts cherating ksb km', 'johnny dullah expn claim mid',
                     'xxxxxxxxx nursyafiq mileage home ksb km', 'xxxxxxxxx nursyafiq mileage home ksb km',
                     'xxxxxxxxx nursyafiq mileage ksb home km', 'prepayment charge roadtax renewal',
                     'prepayment charge roadtax renewal wlq', 'prepayment misc charge roadtax insurance renewal wmj',
                     'prepayment misc charge roadtax renewal wb', 'uesb prepayment road tax insurance le',
                     'uesb prepayment mbs roadmax road tax insurance renewal wrj',
                     'uesb prepayment mbs roadmax roadtax renewal wb', 'uesb prepayment road tax insurance renewal vab',
                     'uesb prepayment road tax insurance renewal wc', 'uesb prepayment road tax insurance renewal wwe',
                     'uesb prepayment roadtax renewal dcn', 'uesb prepayment roadtax renewal wc',
                     'prepayment charge roadtax renewal', 'prepayment charge roadtax renewal wlq',
                     'prepayment misc charge roadtax insurance renewal wmj',
                     'prepayment misc charge roadtax renewal wb',
                     'uesb prepayment misc mbs roadmax road tax insurance renewal wrj',
                     'uesb prepayment misc mbs roadmax roadtax renewal wb',
                     'uesb prepayment misc road tax insurance le',
                     'uesb prepayment misc road tax insurance renewal vab',
                     'uesb prepayment misc road tax insurance renewal wc',
                     'uesb prepayment misc road tax insurance renewal wwe', 'uesb prepayment misc roadtax renewal dcn',
                     'uesb prepayment misc roadtax renewal wc', 'xxxxxxxxx dat hong rings nbr inv cs',
                     'xxxxxxxxx mr diy vernie calipers inv', 'xxxxxxxxx toyosuma auto rubber grease inv cs',
                     'xxxxxxxxx bearing parts rings viton inv cs',
                     'xxxxxxxxx sk hardware polurethane coated glove skhb', 'xxxxxxxxx washer lock',
                     'nurul janna bean beg refill', 'eco shop house cleaning tools', 'akv trading',
                     'emporium labuan lemon bloom detergent', 'tct trading sdn bhd tablecloth inv slb',
                     'tiang peng hardware sdn bhd inv cs', 'xxxxxxxxx norsyukry purchase glove fs home ois',
                     'supply install custom open rack uzmalab', 'transportation charge',
                     'office supplies stationery mm documents file', 'office supplies stationery management file',
                     'office supplies stationery plastics pocket', 'office supplies stationery clipboard plastics',
                     'office supplies stationery duct tape yds silver',
                     'cos maintenance consumabletools way gang trailing socket',
                     'cos maintenance consumabletools socket suis', 'rubber gasket type mtr roll', 'rubber strip steel',
                     'extractor soxhlet ml = units', 'receiver dean stark – ml = units', 'round bottom flask ml = unit',
                     'goforth single leg wire rope sling mt hyr eye hoist hook identification tag',
                     'apm nuclear osl badge radiation worker', 'staff salary director fee ot admin',
                     'staff salary director fee ot scm', 'uesb staff salary gora base yard operations ot',
                     'uesb staff salary gpsd water solutions wim overtime', 'staff salary director fee ot admin',
                     'staff salary director fee ot scm', 'uesb staff salary gora base yard operations ot',
                     'uesb staff salary gora mrc addpay', 'uesb staff salary gora mrc ot',
                     'uesb staff salary gpsd water solutions wim overtime',
                     'lifelong prosperity late payment charges dkrm', 'mbpj assesment tax late charges',
                     'hrdf penalty interest', 'reclass pob late charges cmrc', 'penalty levy charges',
                     'ambank term loan repayment ghazi rm', 'heritage marketing usage', 'heritage marketing usage',
                     'heritage marketing usage', 'heritage marketing usage', 'heritage marketing usage',
                     'heritage marketing usage', 'heritage marketing usage', 'heritage marketing usage',
                     'heritage marketing usage chrg', 'heritage marketing usage chrg', 'heritage marketing usage chrg',
                     'heritage marketing usage chrg', 'heritage marketing usage chrg', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye', 'baker tilly misc exp audit fye',
                     'baker tilly misc exp audit fye',
                     'baker tilly travelling despatch transportation telephone printing photocop', 'pocket expenses',
                     'pocket expenses', 'pocket expenses', 'noblehouse sundry disburment',
                     'xxxxxxxxx print expert sb cs business card', 'printing stationery',
                     'xxxxxxxxx norsyukry purchase measurement equipment lf hardware cs',
                     'xxxxxxxxx norsyukry printing services site visit saba photo', 'crowe kl printing stationery',
                     'badri shah expn claim mid', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing usage chrg',
                     'canon cl clr ink cart', 'canon pg ink cart', 'heritage marketing usage chrg',
                     'heritage marketing usage chrg', 'heritage marketing usage chrg', 'heritage marketing usage chrg',
                     'heritage marketing usage chrg', 'heritage marketing usage chrg', 'heritage marketing usage chrg',
                     'heritage marketing usage chrg', 'heritage marketing usage', 'heritage marketing usage',
                     'heritage marketing usage', 'heritage marketing usage', 'heritage marketing usage',
                     'heritage marketing usage', 'heritage marketing usage shah alam office', 'hp aa ink', 'hp aa ink',
                     'safety pin', 'safety pin', 'ik yellow paper gsm cs', 'mouse cage',
                     'labuan supermarket stationery inv', 'mr diy sdn bhd staples gun inv',
                     'aisya printing geospatial al brouchures tp', 'aisya printing geospatial al brouchures tp',
                     'aisya printing geospatial al brouchures bksa kum',
                     'aisya printing geospatial al poster brouchures career fai tp',
                     'aisya printing geospatial al stickers tp', 'certified true copy stamp inv',
                     'clear sheet protector filing inv xb', 'xxxxxxxxx othman stationery event',
                     'xxxxxxxxx othman stationery event', 'xxxxxxxxx achik sb set roll banting tp',
                     'professional green screen agm inv qs cmxu',
                     'tricor prof fees incurred internal audit services rendered cycle',
                     'nur fatihah print banner buntings camping inv px', 'heritage marketing rental printing chr',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg',
                     'heritage marketing rental printing chrg', 'heritage marketing rental printing chrg labuan office',
                     'third party service expenses', 'office supplies stationery pencil',
                     'office supplies stationery ik natural photo copy paper ream', 'cerberuswi ct wl',
                     'renewal software adobe acrobat pro dc vip cbe', 'accrual microsoft azure admin',
                     'accrual microsoft azure ceo', 'accrual microsoft azure communication',
                     'accrual microsoft azure finance', 'accrual microsoft azure', 'accrual microsoft azure legal',
                     'accrual microsoft azure mecas', 'accrual microsoft azure people', 'accrual microsoft azure qhse',
                     'accrual microsoft azure scm', 'accrual microsoft azure transformation',
                     'prepayment misc charge bp smartcore digital sb',
                     'prepayment misc charge microsoft yearly service subs',
                     'prepayment misc charge sage annual maintenance',
                     'prepayment misc charge veritas ent vault archiving yearly renewal',
                     'prepayment misc charge custom solution exact business software',
                     'prepayment misc charge hr annual software maintenance',
                     'uesb prepayment autocad lt commercial single user annual subscript renewal year fair',
                     'uesb prepayment software adobe subscription lab', 'pc kl purchase sata ssd gb',
                     'sw warrior year acquixxxxxxxxxon extension', 'microsoft renewal estimated price pror',
                     'fc fortigate year unified threat protection utp', 'microsoft renewal estimated price',
                     'microsoft renewal estimated price', 'microsoft renewal estimated price',
                     'azurecsp payperuse subscription', 'prepayment misc charge bp smartcore digital sb',
                     'prepayment misc charge microsoft yearly service subs',
                     'prepayment misc charge reclass fortigate year unified threat protection utp',
                     'prepayment misc charge reclass sofware prepayment license adobe design',
                     'prepayment misc charge rental notebook mystep lenovo ideapad units mo',
                     'prepayment misc charge sage annual maintenance',
                     'prepayment misc charge veritas ent vault archiving yearly renewal',
                     'prepayment misc charge hr annual software maintenance',
                     'reversal prepayment balance custom solution exact business software workflow',
                     'reversal prepayment balance exact souteast asia esl annual fee',
                     'reversal prepayment misc hr annual software maintenance renewal notice',
                     'reversal prepayment exact southeast asia one fee esl exact wholesale dist',
                     'reversal prepayment exact southeast asia one fee esl light user named',
                     'reversal prepayment exact southeast asia one fee esl heavy user named',
                     'reversal prepayment hr annual software maintenance renewal fee expiry',
                     'uesb prepayment misc autocad lt single user annual subscript renew year fair',
                     'uesb prepayment misc software adobe subscription lab', 'cerberuswi forces ct wl jp',
                     'ctes renewal cerebus software well intervention',
                     'optional ap poroperm software installation troubleshooting basic software installation',
                     'poroperm ap pc repair troubleshooting',
                     'autocad lt commercial single user annual subscription renewal contract',
                     'autocad lt renewal year vip number', 'dismantle fee', 'manpower', 'packaging',
                     'trucking ex miri labuan', 'pc wireline aircond service eline logging cabin',
                     'hasran yasin cycle carrage inv', 'nurul janna car maintance abs pump',
                     'nurul janna service maintence bmw', 'hasran yasin cn auto aircond inv cscn services wlq',
                     'muhamad amir car wash', 'xxxxxxxxx xxxxxxxxx pju tyre trading services car services',
                     'syahirah sanz auto service engine oil oil filter atf oil labour cost',
                     'ahmad yunus expn claim mid', 'nur syahirah pc admin',
                     'xxxxxxxxx arifin merz auto garage sdn bhd mrecedes benz wc',
                     'xxxxxxxxx arifin sharikat automatic motors mrecedes benz wc cs', 'ahmad yunus expn claim mid',
                     'cleaning office charges', 'capacitor aircond pws electrical pos', 'door lock level ph hardware',
                     'led downlight cowell electronic cw cs', 'led strip white',
                     'accrual white wash cleaning services uzma tower month',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund lb', 'white wash cleaning svs uzma tower',
                     'white wash cleaning svs uzma tower', 'white wash credit note discount total outstanding',
                     'cleaning office charges', 'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund',
                     'empire damansara jmb service charge sinking fund lb', 'white wash cleaning svs uzma tower',
                     'office sanitisation works uzma lab',
                     'general services supply units air conditioning fan motor faulty champion', 'canon cart black',
                     'canon black toner', 'aircond pump faulty', 'hand rub sanitizing liquid bottles',
                     'kangaroo paint remover', 'air products rental spec gas single cylinder hold cts',
                     'charges air conditioning supply led lighting lab office',
                     'charges general checking supply set led lighting faulty uzma',
                     'charges general services instal checking wiring electrical trip fo',
                     'charges general services outdoor change air compperossor air conditti',
                     'charges install set led lighting wiring faulty uzmalab offic',
                     'checking overhoul top air cond supply set led lighting',
                     'supply install set ceiling led lighting charges air condition le', 'bomba cert',
                     'airconditioning repairing aircond light msq office',
                     'general checking air conditioning sportlight warehouse area',
                     'general services install checking electrical trip led lighting reception',
                     'general services install checking electrical trip mecas aircond leaking',
                     'ton cable puller brand bts mtr diameter mtr wire rope', 'kg cable puller brand bts mtr wire rope',
                     'sw west year key', 'uesb prepayment hb industrial hose hydraulic pneumatic unit',
                     'uesb prepayment elmar line size kit gie injection cable cuttercylind',
                     'claimable rate malaysian local participant background screening shahari',
                     'uesb prepayment misc hb industrial hose hydraulic pneumatic unit',
                     'uesb prepayment misc elmar line size kit gie injection cable cuttercylind',
                     'kimble kimax heavy duty glass solution bottle carboy gallon', 'srew filter retaining',
                     'spinner tool bds pps jewel brg', 'assy shaft spinner jewel bearing', 'plug flushing port',
                     'filter gauze', 'cwhs spare cwh pcsb psu tle uw meter progd',
                     'prts spare prt pcsb psu tle uw meter progd', 'scr skt hd mmlg ms', 'pin spirol mck dia lg',
                     'pin spirol mck dia lg', 'ring fkm imp ms', 'dust collector point frequency times per year',
                     'fume hood points frequency per year',
                     'local exhaust ventilation monitoring fume hood frequency per year',
                     'prepare document renew compressor sl pmt jkkp dosh', 'cargo slings', 'crane tonnes',
                     'crane tonnes ot', 'forklift tonnes', 'forklift tonnes ot', 'labour base operative rate',
                     'labour base operative rate', 'labour chargehands rate', 'labour chargehands rate',
                     'labour crane operator', 'labour crane operator rate', 'labour forklift operator rate',
                     'labour transport operator rate', 'labour transport operator rate', 'transport lowloaders axles',
                     'transport lowloaders axles ot', 'radioactive source leak test', 'sas dbl bx go', 'sas dbl pn go',
                     'sas swivel next gen go bx pn', 'sas knuckle joint assy dbl bj go', 'sas btn pn go bx',
                     'sas btn pn hp go bx dg',
                     'safety equipment survival equipment rescue boat liferaft etc first aid box',
                     'safety equipment survival equipment rescue boat liferaft etc stretcher',
                     'freight charges air freight transportation', 'skit kit dbl go bx', 'skit kit double go pin',
                     'skit kit knuckle joint assy bj go', 'skit kit go low prs fire sub',
                     'skit kit go high prs fire sub', 'skit kit swivel go bx go pn',
                     'supply labour materials remove existing flexible hose replace lab sink area mecas',
                     'tonne crane vdw uv', 'tonne lorry ppe', 'tonne lorry ppe uv', 'tonne lorry saa',
                     'tonne lorry saa uv', 'tonne lorry saa uv', 'feet trailer jtp uv', 'asb gate fee cost plus',
                     'asb gate fee cost plus', 'overtime rate tonne lorry ppe uv', 'overtime rate uu',
                     'overtime rate uv',
                     'repair internal water leak supply labour materials hack exising affected walls',
                     'wash basin replacement supply new wash basin inclusive connecting existing pipes',
                     'local calibration',
                     'ranger exp digital radiation detector external pancake probe brand radiation alert usa',
                     'dust collector point frequency times per year final payment',
                     'ap eval repair evaluation repair ap unit consists material', 'labour hours hr discounted hr',
                     'consultant fee repair hydraulic pumps', 'srvce em maintenance repair equipment hydraulic pumps',
                     'site testing units rccb', 'survey meter', 'fishing head assy art type', 'redress kit level art',
                     'redress kit level art', 'redredd kit level art', 'ring buid set', 'ring build set ',
                     'upper sub sat bxx', 'connector assembly long sat', 'insulator upper go head',
                     'connector assembly long sat', 'contact plate go head', 'insulator plug upper go head',
                     'contact pin go head', 'connector assembly short sat', 'tube wire protection sat dxx',
                     'ring build list sat', 'ring build set sat', 'ring build kit sat', 'pin banana mm male mm',
                     'pin banana mm male mm', 'insulator lower head connector', 'insulator lower head inner short',
                     'cup insulator head', 'connector head go type', 'insulator lower head ppl type',
                     'connector lower head go', 'connector un', 'contact rod', 'contact rod mm banana pin',
                     'wave spring od id', 'spring compression dia', 'screw skt cap hd mm', 'circlip internal',
                     'washer mm plain', 'snap ring mm internal', 'wire ptfe white awg type',
                     'lfh silicone sleeving long sat axx id mm', 'lfh silicone sleeving', 'fluorocarbon boot assembly',
                     'retaining sleeve feedthrough', 'mm desolder braid general use see', 'site testing units rccb sst',
                     'lifting services unit binder kbf gf second floor via staircase weight kg',
                     'qb bladder accumulator', 'qcs qhp charge kit qcs', 'svc pcp topside specification',
                     'delivery ksb kmn', 'pir sensor', 'pir complete unit',
                     'testing tools magnetic wand blue body white logo', 'testing tools calibration hose per meter',
                     'testing tools metane lel air litre', 'testing tools zero air litre',
                     'testing tools cylinder regulator cc min', 'skit shck sub spring type', 'washer cablehead',
                     'cblhd cone brass ln', 'sas cblhd cw ln fn', 'delivery charges labuan express shipping',
                     'flapper hydraulic tool trap id', 'ring acme', 'magnetic wand', 'tt kit ext ind',
                     'calibration hose per meter', 'qt kit id lw quick test sub', 'cylinder regulator cc min',
                     'qc nipple npt male valved', 'methane lel air litre', 'qc coupler npt male ref vhc mv',
                     'zero air litre', 'needle valve npt male npt female psi working pressure std',
                     'kit aw pump haskel incl fluid section seal kit air section seal kit air valve', 'ring connection',
                     'back ring connection', 'calibration kit', 'pir complete set',
                     'pcb tested assy gamma gun elec geiger', 'sas cent go springs', 'sas dbl pn go',
                     'skit kit complete', 'skit kit centraliz', 'skit kit double go pin', 'somf spring centralizer dia',
                     'somf spring centralizer dia', 'adapter autoclave parker hp male npt male',
                     'quick coupling parker npt female screw wp bar', 'spear grapple nom ff', 'capacitor', 'ic cy pxi',
                     'ic', 'ic opa aid', 'ic soic', 'lamp', 'knob', 'sds hourly labor charge', 'shipping costs dg un',
                     'total freight', 'sentergy probe', 'somf spring centralizer dia', 'skit', 'skit lr', 'skit wr',
                     'analytical balance range serial', 'analytical balance range serial',
                     'liquid glass thermometer range ° ° control number', 'standard weight range control number',
                     'forklift tonnes', 'labour forklift operator rate', 'bee hing minimart cat brush',
                     'hoi peng hardware kobelco pad lock set inv cs', 'kedai kita glossy paper',
                     'layangan shopper jumbo clip inv', 'lintasan nurani wooden pallet inv', 'strecth film spary inv',
                     'tct trading sdn bhd socket water boiler inv slb',
                     'tian peng hardware rubber pvc iron welding inv cs',
                     'tian peng hardware sdn bhd pvc coupling inv cs', 'yc engineering supply plastic inv',
                     'dewalt hand drill lithium ion ah', 'fluke meter',
                     'maintenance consumable tools disposable earplug',
                     'maintenance consumable tools half facepiece respirator medium',
                     'maintenance consumable tools particulate filter',
                     'maintenance consumable tools twister hand glove', 'pilot jotun black', 'pilot jotun grey',
                     'pilot jotun yellow', 'pvc apron', 'pvc packing tape', 'silver duct tape',
                     'tool machinery part opex step bin', 'welding machine arc ge', 'custom inward outward',
                     'forklift tonnes', 'forklift tonnes ot', 'garbage removal', 'grass cutter inclusive operation',
                     'labour forklif operation rate', 'labour forklif operation rate', 'servicing cylinder',
                     'mm makita ds spade handle drill', 'mm ft ft plywood', 'mm ddf sfx cordless driver drill',
                     'cw tapping screw pcs box', 'purchase item containers refurbishment base yard',
                     'labuan supermarket safety plig plug door lock', 'tct trading sdn bhd glue padlock',
                     'cos maintenance hardware industrial fan', 'cos maintenance hardware mild steel angle bar',
                     'cos maintenance hardware mild steel hollow', 'tool machinery part opex angle bar saiz mm',
                     'tool machinery part opex cutting disc size mm box',
                     'tool machinery part opex expended metal mesh saiz', 'tool machinery part opex heavy duty hinge',
                     'tool machinery part opex hollow saiz mm', 'tool machinery part opex magnet square welding',
                     'tool machinery part opex simendrill bit saiz mm mm', 'tool machinery part opex wall plug saiz mm',
                     'tool machinery part opex welding rod china mm', 'maintenance office equip fresco kg freon gas',
                     'maintenance office equip mapp gas map', 'cos servicecost thirdparties rodent control',
                     'supply install air condition wall mounted split unit acson hp',
                     'assembly point signboard cw hollow', 'delivery installation',
                     'hse statistic signboard cw hollow cw aluminium holder', 'reverse parking signboard cw hollow',
                     'uzma sign board cw hollow', 'wireline lab signboard', 'wireline signboard',
                     'rahmat bernas security security chrg labuan yard',
                     'rahmat bernas security security chrg labuan yard sst', 'charges uzmalab security guards',
                     'accrual enforce security security services charges security dkrm house',
                     'accrual sri lara joint security services security services charges',
                     'enforce security services security svs chrg green ville',
                     'sri lara joint security services security chrg', 'uesb prepayment secretary monthly retainer fee',
                     'rahmat bernas security security chrg labuan yard',
                     'rahmat bernas security security chrg labuan yard sst', 'charges uzmalab security guards',
                     'accrual enforce security security services charges security dkrm house',
                     'accrual sri lara joint security services security services charges',
                     'enforce security services security svs chrg green ville',
                     'reversal accrual enforce security security services charges security dkrm house',
                     'reversal accrual enforce security security services charges security dkrm house',
                     'reversal accrual sri lara joint security services security services charges',
                     'reversal accrual sri lara joint security services security services charges',
                     'aia aso aso claim excess billing', 'accrual staff insurance ghs', 'accrual staff insurance gtl',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing group term life ub',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia aia billing ghs premium admin fee',
                     'prepayment aia renewal aia group term life uesb consultant gora',
                     'prepayment aia renewal aia group term life uesb consultant ipm',
                     'prepayment aia renewal aia group term life uesb consultant lab',
                     'aia adjustment billing ghs premium admin fee',
                     'aia adjustment billing gtl premium group term life', 'aia adjustment billing aia group term life',
                     'aia aia billing ghs premium admin fee', 'aia aso aso claim excess billing uesb',
                     'aia adjustment group term life uesb consultant',
                     'aia adjustment group term life uesb consultant ipm sst',
                     'aia adjustment group term life uesb consultant gora',
                     'aia adjustment group term life uesb consultant gora sst',
                     'aia adjustment group term life uesb consultant ipm', 'aia adjustment billing group term life',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb',
                     'aia adjustment billing group hospitalization uesb', 'aia adjustment billing group term life',
                     'aia adjustment billing group term life', 'aia adjustment billing group term life',
                     'aia adjustment billing group term life', 'aia adjustment billing group term life',
                     'aia adjustment billing group term life', 'aia billing ghs premium admin fee uesb',
                     'accrual staff insurance ghs', 'accrual staff insurance gtl',
                     'prepayment insurance charge aia billing aia group term life',
                     'prepayment insurance charge aia billing aia group term life',
                     'prepayment charge staff insurance ghs', 'prepayment charge staff insurance ghs sst',
                     'prepayment charge staff insurance gtl', 'prepayment charge staff insurance gtl sst',
                     'prepayment charge aia renewal billing aia gtl', 'prepayment charge aia billing ghs premium admin',
                     'prepayment charge aia renewal billing aia gtl', 'prepayment charge aia billing ghs premium admin',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing ghs premium admin fee',
                     'prepayment insurance aia billing group term life ub',
                     'prepayment aia aia billing group term life uesb',
                     'prepayment aia aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb',
                     'prepayment aia billing group term life uesb uesb',
                     'prepayment aia billing group term life uesb uesb sst',
                     'prepayment aia billing group term life uesb uesb sst',
                     'prepayment aia billing group term life uesb', 'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing group term life uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'prepayment aia billing ghs premium admin fee uesb',
                     'prepayment aia billing ghs premium admin fee uesb sst',
                     'xxxxxxxxx staff engagement restaurant od',
                     'xxxxxxxxx today medan pyarmacy newgene covid saliva test kit tp',
                     'xxxxxxxxx sk hardware safety glasses skhb', 'xxxxxxxxx staff engagement restaurant od',
                     'hanie artisan playground cookhouse kay fatima farewell',
                     'hanie artisan playground cookhouse kay fatima farewell',
                     'hanie artisan playground cookhouse kay fatima farewell',
                     'hanie thai tuk tuk restaurant lunch new joiner sofrina', 'mazlinda token new born',
                     'xxxxxxxxx alfeizal home solar svp sharing session ayam penyet',
                     'xxxxxxxxx alfeizal home solar uzma sharing session warung ambo sa',
                     'kama labuan base visit base operations dep lunch', 'cleaning staffhouse', 'house cleaning staff',
                     'tengku xxxxxxxxx laundry cloth', 'century superstore hup seng cracker', 'ng teck koon gula',
                     'ng teck koon mineral water mlx',
                     'nur adilah bereavement fund claim entitlement father passed away',
                     'rancha rancha aerated water refill inv', 'rancha rancha aerated water refill inv',
                     'rancha rancha aerated water refill inv', 'speed mart sb pantry item date',
                     'speed mart sb pantry item date', 'speed mart sb pantry item date',
                     'speed mart sb pantry item date', 'speed mart sb pantry item date',
                     'speed mart sb pantry item date', 'speed mart sb pantry item date',
                     'aeon co sdn bhd pantry item date', 'xxxxxxxxx eleese expn claim mid', 'muhazam expn claim mid',
                     'rhb cc drms statement date', 'rhb cc drms lotus stotes pantry items leve cpmy',
                     'rhb cc drms lotus stotes pantry items leve cpmy', 'pc kl pantry iteam', 'pc kl pantry supplies',
                     'pc kl staff pantry expenses', 'dust mask', 'livex safety goggle',
                     'norsusanty kuih cara berlauk keria koci inv', 'norsusanty kuih penjaram cod inv',
                     'norsusanty roti jala plain kg kari ayam cod inv', 'plus ml km', 'basic pantry', 'basic pantry km',
                     'basic pantry km', 'basic pantry km', 'spritzer mineral water pskm',
                     'spritzer mineral water ml pskm', 'ubat mencegah jentik jentik abate',
                     'emporium labuan shopping mart inv', 'haphuat trading consumable pantry inv',
                     'rancha rancha aerated water refill water inv', 'yun kwang family mart consumable pantry inv',
                     'yun kwang family mart consumable pantry inv', 'yun kwang family mart consumable pantry inv',
                     'yun kwang family mart consumable pantry inv', 'yun kwang family mart consumable pantry inv',
                     'century superstore consumable pantry inv', 'rancha rancha aerated water refill water inv',
                     'syarikat perniagaan jason besen gayung inv', 'xxxxxxxxx othman lunch uzam svp event committee',
                     'xxxxxxxxx kamarul apple butter meals inv', 'xxxxxxxxx kamarul four hundred rabbits meals inv',
                     'xxxxxxxxx kamarul harrods meals satellite biz trip inv nt',
                     'xxxxxxxxx kamarul hunger vky restaurant dinner ankara turkiye trip inv',
                     'xxxxxxxxx kamarul pot rice mezocha ltd meals', 'xxxxxxxxx xxxxxxxxx white sand cafe drink staff',
                     'xxxxxxxxx xxxxxxxxx whitesand cafe drink dk datin shahrin', 'syazwan marriage gift',
                     'balance payment bowling urc inv ou', 'ksb trip lunch pax mk chukai clm nego', 'pantry items',
                     'pantry items', 'rhb cc drms statement date', 'samuel leonard token new born',
                     'zah farewell bungalow mc dinner', 'zah farewell daun petals flowers inv',
                     'offshore duffle bag size wheel',
                     'safety workwear jacket colour orange company logo malaysia flag size',
                     'bg wireline pcsb tcxg kup', 'bg surtuhanjaya tenaga uzma kuala muda apnkli charges',
                     'xxxxxxxxx amilya payment lhdn stamping iws package',
                     'xxxxxxxxx amilya payment lhdn stamping repsol well test',
                     'xxxxxxxxx amilya payment lhdn stamping cpoc jack drilling',
                     'xxxxxxxxx amilya payment lhdn stamping hess hpht jack',
                     'xxxxxxxxx amilya payment lhdn stamping mash four',
                     'xxxxxxxxx amilya payment lhdn stamping nde en shahrum',
                     'charges bg pttep sabah apnkli bg extension', 'bg extension pengkalan bekalan kemaman ibg',
                     'xxxxxxxxx amilya payment lhdn stamping loa extension contract jack',
                     'xxxxxxxxx amilya payment lhdn stamping ltsa', 'hasran yassin reaload touch go',
                     'muhamad amir toll gcpv training', 'xxxxxxxxx haziq toll', 'xxxxxxxxx haziq toll',
                     'xxxxxxxxx xxxxxxxxx touch go', 'xxxxxxxxx xxxxxxxxx touch go', 'xxxxxxxxx xxxxxxxxx touch go',
                     'muzaffar touch go', 'xxxxxxxxxza hess btgb toll', 'xxxxxxxxxza hess btgb toll',
                     'xxxxxxxxxza pcsb kacak parking', 'xxxxxxxxxza pcsb kacak toll', 'xxxxxxxxxza pttep toll',
                     'xxxxxxxxxza pttep sirung toll', 'sazlida lunch meeting seah la moon ord',
                     'zulkipli toll kl kemaman kl', 'xxxxxxxxx syahid parking claim', 'xxxxxxxxxzly klcc parking',
                     'xxxxxxxxxzly klcc parking', 'xxxxxxxxxzly klcc parking', 'xxxxxxxxxzly klcc parking',
                     'xxxxxxxxxzly klcc parking', 'xxxxxxxxx rosli parking', 'xxxxxxxxx rosli toll',
                     'xxxxxxxxxt jamali parking hotel', 'xxxxxxxxxt jamali parking hotel office',
                     'xxxxxxxxxt jamali toll kemaman kl', 'xxxxxxxxxt jamali toll kl kemaman',
                     'xxxxxxxxx nursyafiq parking klcc meeting client exxon',
                     'xxxxxxxxx nursyafiq parking klcc meeting client exxon',
                     'xxxxxxxxx rxxxxxxxxx toll home kemaman home', 'xxxxxxxxx rxxxxxxxxx toll home kemaman home',
                     'xxxxxxxxx farhaan parking klcc workshop tag petronas event', 'xxxxxxxxx farhaan toll',
                     'xxxxxxxxx farhaan toll', 'xxxxxxxxx hilmy toll fare', 'shahidan ramli toll',
                     'xxxxxxxxx othman toll', 'nur iza travelling toll', 'xxxxxxxxx xxxxxxxxx parking vallet avenue',
                     'xxxxxxxxx xxxxxxxxx parking vallet klcc', 'xxxxxxxxx xxxxxxxxx touch go',
                     'xxxxxxxxx xxxxxxxxx touch go', 'xxxxxxxxx xxxxxxxxx touch go reload',
                     'xxxxxxxxx xxxxxxxxx touch go reload', 'xxxxxxxxx arifin top',
                     'xxxxxxxxx arifin top oga event kl convex parking', 'sazlida parking mogsc meeting',
                     'sazlida parking mogsc meeting', 'ksb trip vellfire tng mk chukai clm nego',
                     'xxxxxxxxx nursyafiq parking klcc meeting client exxon',
                     'xxxxxxxxx nursyafiq parking seah office seah kickoff meeting', 'xxxxxxxxx nursyafiq toll',
                     'xxxxxxxxx nursyafiq toll', 'xxxxxxxxx nursyafiq toll', 'uesb prepayment misc charge',
                     'tropical offshore emergency training compressed air emergency adh',
                     'terengganu safety bosiet ca ebs tsbb physical', 'disc skim bantuan latihan khas sblkhas',
                     'offshore well abandonment plug abandonment decommissioning khalieff fath',
                     'offshore well abandonment plug abandonment decommissioning xxxxxxxxx nors',
                     'ots pcsb permit work ptw level xxxxxxxxx zuriadi nazirul faiz',
                     'basic rigging slinging banksman person', 'msts basic rigging slinging banksman akasyah nazirul',
                     'msts basic rigging slinging banksman xxxxxxxxx faidhi',
                     'optimal leadership potential identification',
                     'uesb prepayment velesto accredited course learning iwcf well interention',
                     'uesb prepayment borneo safety banksman api approve lawrence',
                     'uesb prepayment borneo safety designated first aider cer',
                     'uesb prepayment borneo safety rigger training simon lawrence',
                     'uesb prepayment borneo safety rigger training afzan xxxxxxxxx faris',
                     'uesb prepayment kinabalu train combined package rigging slinging rigg',
                     'uesb prepayment msts asia training designated first aider',
                     'uesb prepayment rhazes iwcf well intervention pressure control day',
                     'uesb prepayment sequ tas basic opito approve mohamad helmi',
                     'uesb prepayment sequ tas basic opito approved abdul halim',
                     'uesb prepayment sequ tas tropical bosiet ca ebs initial deployment tr',
                     'uesb prepayment sequ tas tropical bosiet ca ebs initial deployment tra',
                     'terengganu safety breathing apparatus certification fittest rpe',
                     'terengganu safety breathing apparatus certification fittest rpe',
                     'terengganu safety lps sshe induction online lawrence',
                     'msts emergency training compressed air emergency breathing system',
                     'petronas technical training pcsb permit work ptw level pax',
                     'terengganu safety foet ca ebs tsbb physical muh',
                     'uesb prepayment misc borneo safety banksman api approve lawrence',
                     'uesb prepayment misc borneo safety designated first aider cer',
                     'uesb prepayment misc borneo safety rigger training simon lawrence',
                     'uesb prepayment misc borneo safety rigger training afzan xxxxxxxxx faris',
                     'uesb prepayment misc kinabalu train combined package rigging slinging rigg',
                     'uesb prepayment misc msts asia training designated first aider',
                     'uesb prepayment misc rhazes iwcf well intervention pressure control day',
                     'uesb prepayment misc sequ tas basic opito approve mohamad helmi',
                     'uesb prepayment misc sequ tas basic opito approved abdul halim',
                     'uesb prepayment misc sequ tas tropical bosiet ca ebs initial deployment tr',
                     'uesb prepayment misc sequ tas tropical bosiet ca ebs initial deployment tra',
                     'uesb prepayment misc velesto accredited course learning iwcf well interention',
                     'harness iwcf wipc virtual shaharizak wireline crew', 'msts tfoet ebs tsbb ca ebs osmond louis',
                     'msts tfoet ebs tsbb ca ebs mohd anezam abdul masah',
                     'msts compressed air emergency breathing system tropical basic offshore safety induction',
                     'bsts opito approved dunstan alvin ak randie dpm', 'sribima ca ebs opito akasyah olis',
                     'sribima tfoet opito ebs tsbb akasyah olis',
                     'provision one day radiation safety awareness training course participants',
                     'msts basic training opito approved suhardi bin wahab',
                     'velesto accredited course virtual learning iwcf siti nabilah binti zainuddin',
                     'velesto energy accredited course virtual learning iwcf well intervention prssrecontrol',
                     'tstc breathing apparatus certification', 'tstc loss prevention system',
                     'tstc loss prevention system',
                     'terengganu saftety loss prevention system respiratory fit test exxon job mobilization',
                     'msts compressed air emergency breathing system caebs initial deployment training opito dody',
                     'terengganu safety breathing apparatus certification dody',
                     'terengganu safety loss prevention system tuan mohd tarmizi',
                     'velesto accredited course virtual learning iwcf well intervention pressure control level',
                     'tstc breathing apparatus cert irfan azrul', 'tstc vreathing apparatus cert amir',
                     'tstc breathing apparatus certification siti nabilah ideris',
                     'tstc brething apparatus certification shahurin',
                     'tstc compressed air emergency brething system ideris faris',
                     'tstc rigging slinging safety loss prevention system',
                     'tstc foet ebs tsbb compressed air emergency breathing siti nabilah',
                     'xxxxxxxxx land transport li hua hotel pttep site kwo kok bkss',
                     'xxxxxxxxx kwo kok land transport li hua hotel pttep bkss',
                     'xxxxxxxxx meal allowance bennet tan days ref', 'xxxxxxxxx meal allowance bennet tan days',
                     'xxxxxxxxx meal allowance robinson days ref', 'xxxxxxxxx meal allowance forrobinson days',
                     'xxxxxxxxx taxi klia home home', 'kama labuan base visit flight klia labuan labuan klia slrqw',
                     'labuan base visit grab home klia', 'labuan base visit grab hotel labuan airport',
                     'labuan base visit grab klia home', 'muhd shafiq air asia ride rm rm',
                     'muhd shafiq flight mas ur kl lbn kl', 'muhd shafiq subsistance half day',
                     'shahidan ramli airasia ride rm rm', 'shahidan ramli flight kl lbn kl mas fp',
                     'shahidan ramli subsistence half day rm rm', 'adrian temporary replacementqhse labuan days',
                     'xxxxxxxxx haziq subsistance rm rm', 'travelling', 'kama kemaman yard visit subsistance allowance',
                     'kama labuan base visit subsistance allowance', 'sazlida grab mogsc meeting',
                     'zulkipli subsistence allowance days', 'mas flight staff abdullah xxxxxxxxx xxxxxxxxxan',
                     'mas flight ticket abdullah xxxxxxxxx xxxxxxxxxan', 'mas ticket bali hasmadi iwuah',
                     'xxxxxxxxxan perdiem kemaman days', 'xxxxxxxxxan perdiem kl',
                     'xxxxxxxxxan perdiem labuan kl kemaman', 'xxxxxxxxxan tic kemaman tbs bus',
                     'xxxxxxxxxan trav tbs termnal klia bus tic', 'erl train kl sentral – klia',
                     'xxxxxxxxx rosli subsistance allowance engagement pcsb',
                     'xxxxxxxxx rosli subsistance allowance engagement pcsb', 'hasmadi bus tic kemaman tbs sani',
                     'hasmadi bus tic tbs klia tbs', 'xxxxxxxxxt jamali subsistance allowance kl days',
                     'juani bus kemaman tbs kl sani', 'juani bus tbs kemaman kl tbs', 'juani bus tbs klia kl tbs',
                     'juani klia transit klia tbs kl', 'xxxxxxxxx rxxxxxxxxx subsistance claim per diem days',
                     'xxxxxxxxx farhaan perdiem days', 'xxxxxxxxx norsyukry grab pdjt suite hotel',
                     'xxxxxxxxx norsyukry perdiem days', 'xxxxxxxxx norsyukry perdiem days',
                     'xxxxxxxxx norsyukry taxi grand putra hotel pdjt inv', 'abdul hafiz expn claim mid',
                     'teik kian salary', 'xxxxxxxxx hilmy subsistance allowance day trip', 'shahidan ramli subsistence',
                     'adrian temporary replacement qhse labuan days', 'aisya subsistance rm rm',
                     'xxxxxxxxx othman orange rules launching perdiem',
                     'xxxxxxxxx othman hse engagemnt meeting per diem', 'xxxxxxxxx othman hsems audit perdiem',
                     'xxxxxxxxx othman mpm pcsb engagement per diem',
                     'nur iza jabatan air sabah invitation present travelling erl klia',
                     'nur iza jabatan air sabah invitation present travelling erl klia', 'nur iza subsistance',
                     'nur iza subsistance', 'xxxxxxxxx alfeizal subsistance allowance',
                     'xxxxxxxxx alfeizal subsistance allowance', 'xxxxxxxxx xxxxxxxxx flight labuan kl mas',
                     'xxxxxxxxx xxxxxxxxx flight kul lbn mas yih', 'xxxxxxxxx xxxxxxxxx perdiem claim night',
                     'express rail klia', 'nur fatihah contract execution hse audit contractor performace perdiem',
                     'nur fatihah grab car fee klia', 'nur fatihah uzma orange rules jom patuh tegur per diem',
                     'xxxxxxxxx arifin grab receipt', 'adham razali perdiem kemaman msts cherating',
                     'adham razali perdiem kemaman msts cherating',
                     'xxxxxxxxx rosli subsistance allowance business partner engagement',
                     'xxxxxxxxx rosli subsistance allowance patuh tegur pcsb',
                     'azhar bin mohamad shahrin per diem ksb msts cherating ksb', 'teik kian salary',
                     'kamarul redzuan expn claim mid', 'xxxxxxxxx nursyafiq subsistance claim patuh tegur pcsb',
                     'xxxxxxxxx nursyafiq subsistane claim business partner engagement',
                     'lab transportation logistics mob demob', 'sayu travel flight khairul fariha kk lbu',
                     'sayu travel flight nurul amirah kul lbu', 'sayu travel flight ahmad ridhuan',
                     'sayu travel flight charge andreas rizky lbu kul', 'sayu travel flight charge khalieff fathiee',
                     'sayu travel flight charge mohd fairus lbu kul', 'sayu travel flight charge mohd fairus',
                     'sayu travel flight charge well solutions staff', 'sayu travel transaction fee',
                     'sayu travel transaction fee', 'sayu travel transaction fee',
                     'xxxxxxxxx xxxxxxxxx kl surabaya aa wlma', 'xxxxxxxxx mas ghazay surabaya kl lnsy',
                     'xxxxxxxxx hotel surabaya airport', 'xxxxxxxxx perdiem surabaya days',
                     'xxxxxxxxx taxi surabaya airport hotel sz', 'muzaffar perdeim uzma kuantan kerteh kuatan',
                     'muzaffar perdiem kuantan uzma pj', 'ahmad yunus yunus kl istambul vacation allowance',
                     'xxxxxxxxx kamarul entry fee gaucho tower bridge inv',
                     'xxxxxxxxx kamarul flight ankara london inv mma', 'xxxxxxxxx kamarul flight london kl inv mma',
                     'xxxxxxxxx kamarul taxi airport transfer inv', 'xxxxxxxxx kamarul taxi inv',
                     'zaleha mas kul london xxxxxxxxx amran gyi', 'zaleha mas kul london zaleha ym',
                     'perdeem trip indonesia', 'xxxxxxxxx arifin batik air jakarta xxxxxxxxx ros aliff',
                     'xxxxxxxxx arifin batik air travel insurance xxxxxxxxx', 'xxxxxxxxx arifin batik air flight food',
                     'xxxxxxxxx arifin grab receipt idr', 'xxxxxxxxx arifin grab receipt idr',
                     'xxxxxxxxx arifin grab receipt idr', 'xxxxxxxxx arifin grab receipt idr',
                     'xxxxxxxxx arifin grab receipt idr', 'xxxxxxxxx arifin grab receipt idr',
                     'xxxxxxxxx arifin grab receipt idr', 'xxxxxxxxx arifin grab receipt idr',
                     'tours flight rahmat wobisono kul cgk',
                     'ultima ear muff helmet mounted brand msa pyramex must fitted full bri',
                     'offer king clear safety glasses pcs box',
                     'offer proguard safety helmet sirim yellow plastic harness side lock abs shel',
                     'offer size nitrile gloves', 'black glove ansell', 'delivery charges ksb',
                     'ppe coverall orange size name tag company logo', 'ppe coverall size xxl',
                     'ppe jacket houston fr jacket long sleeve size', 'ppe jacket orange nametag uzma logo size xl',
                     'ppe jacket orange nametag uzma logo size xl',
                     'ppe nomex coverall orange nametag uzma logo size xl', 'safety shoes oscar size uk size uk',
                     'safety boot red wing pecos code size uk',
                     'coverall iiia colour orange company logo malaysia flagbrand nomex name ismail size xl',
                     'impact glove kong glove size', 'uvex safety spectacles vo colour blue orange clear lense',
                     'ear muff honeywell must fitted slotted full brim helmet msa',
                     'full brim hard hat points chin strap brand msa color white', 'ppe safety boots rw size',
                     'redwing pecos old part num size uk pr uk pr', 'offer msa gard green hard hat manufacturing',
                     'safety boot red wing pecos code size uk', 'safety boot red wing pecos code size uk',
                     'full brim hard hat points chin strap', 'sabah electricity electricity chrg labuan yard',
                     'tnb electricity charge ksb', 'tnb electricity charge ksb', 'charges utilities electricity days',
                     'tnb electricity bill staffhouse', 'tnb electricity bill staffhouse',
                     'sabah electricity electricity chrg labuan yard', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg ub', 'tnb electricity charge ksb',
                     'sabah electricity electricity chrg labuan yard', 'charges utilities electricity days',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'accrual mammoth electricity charges uzma tower', 'accrual mammoth electricity charges uzma tower',
                     'mammoth empire electricity charg', 'mammoth empire electricity charg',
                     'mammoth empire electricity charg', 'mammoth empire electricity charge',
                     'mammoth empire electricity charge', 'mammoth empire electricity charge',
                     'mammoth empire electricity charge', 'mammoth empire electricity charge',
                     'mammoth empire electricity charge', 'mammoth empire electricity charge',
                     'mammoth empire electricity charge', 'mammoth empire electricity charge ub',
                     'reverasl mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower',
                     'reversal mammoth electricity charges uzma tower', 'indah water konsortium waste disposal chrg',
                     'indah water konsortium waste disposal chrg', 'indah water konsortium waste disposal chrg',
                     'indah water konsortium waste disposal chrg', 'indah water konsortium waste disposal chrg',
                     'indah water konsortium waste disposal chrg', 'indah water konsortium waste disposal chrg',
                     'indah water konsortium waste disposal chrg', 'indah water konsortium waste disposal chrg',
                     'indah water konsortium waste disposal chrg', 'indah water konsortium waste disposal chrg',
                     'jba wilayah water bill uzma office labuan', 'syrkt air terengganu water bill staffhouse',
                     'syrkt air terengganu water bill staffhouse', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'empire damansara jmb water chrg',
                     'empire damansara jmb water chrg', 'water consumption yard',
                     'jba wilayah water bill uzma office labuan', 'pangkalan bekalan water consumption',
                     'charges utilities water', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'edjm water charges level', 'edjm water charges level',
                     'edjm water charges level', 'reveral edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'reversal edjm water charges level',
                     'reversal edjm water charges level', 'telekom malaysia internet charge uzma tower',
                     'telekom internet labuan', 'charges utilities phone internet', 'telephone internet',
                     'maxis telephone chrg dn tel', 'maxis telephone chrg en xxxxxxxxx tel', 'maxis telephone chrg',
                     'tt dotcom internet usage uzma tower', 'tt dotcom office telephone bill',
                     'pangkalan bekalan highspeed broadband hsbb', 'telekom malaysia internet charge uzma tower',
                     'telekom internet labuan', 'charges utilities phone internet',
                     'prepayment misc charge tt dotcom office internet charges',
                     'reversal prepayment tt dotcom office internet charges', 'tt dotcom office telephone bill']

        # Tokenize each sentence into words
        sentence_words = [word.lower() for sentence in sentences for word in sentence.split()]

        # Tokenize the OCR text into words
        ocr_words = text.split()

        # Count the occurrences of each word in OCR text
        ocr_word_count = {word: ocr_words.count(word) for word in set(ocr_words)}

        # Find the common words between the sentences and OCR text
        common_words = []
        for word in sentence_words:
            if word in ocr_word_count and ocr_word_count[word] > 0:
                common_words.append(word)
                ocr_word_count[word] -= 1

        # Create a new list with each occurrence of the common words
        filtered_text = ' '.join(common_words)
        filtered_text2 = [filtered_text]

        # Make predictions on the new test data
        predictions = loaded_model.predict(filtered_text2)

        return predictions[0]


def is_float(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def extract_grand_total(ocr_result):
    grand_total = None
    largest_value = float('-inf')  # Initialize with negative infinity

    currencies = "rm|myr"
    amount_regex = fr"(({currencies})? *(\d+\.\d+)|(\d+\.\d+) *({currencies})?)"

    ocr_result_lower = ocr_result.lower()

    grand_total = 0
    largest_value = 0

    # Number of amount detected
    found = 0

    keywords = ["grand total", "order total", "parking fee", "total outstanding amount", "total"]
    for keyword in keywords:
        if keyword in ocr_result_lower:
            # Try to find a numeric value next to or in the same row as the keyword
            numeric_pattern = re.compile(fr"\b{keyword}[\s:]*{amount_regex}[^\n]*")
            numeric_match = re.search(numeric_pattern, ocr_result.lower())
            if numeric_match:
                found = found + 1
                group2 = numeric_match.group(2)
                group3 = numeric_match.group(3)

                if is_float(group2):
                    numeric_value = float(group2)
                    currency = group3
                else:
                    numeric_value = float(group3)
                    currency = group2
                if numeric_value > largest_value:
                    largest_value = numeric_value
                    grand_total = largest_value

    if found == 0:
        # No currency & amount found with regex.
        # Now find the largest amount
        amount_pattern = re.compile(fr"\d+\.\d+")
        matches = re.findall(amount_pattern, ocr_result_lower)
        grand_total = max(map(lambda v: float(v), matches))

    return grand_total


def extract_text_files(text):
    grand_total = extract_grand_total(text)

    return f"{grand_total:.2f}"


# Get input numbers from command line arguments
file_name = str(sys.argv[1])
path = r'C:\xampp\htdocs\lightxpense\uploads\\'
image_name = path + file_name

output = process(image_name)
output = " ".join(line.strip() for line in output.splitlines())

# Call function:
predicted_label = process_text(output)

# Call function:
amount = extract_text_files(output)

# Return as JSON-encoded string
if predicted_label:
   returnDict = {
        'status': 200,
        'label': predicted_label,
        'amount': amount
    }
else:
    returnDict = {
        'status': 400,
        'label': 'None',
        'amount': 'None'
    }

returnDict = json.dumps(returnDict)

print(returnDict)
