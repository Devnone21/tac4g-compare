#!/usr/bin/env python3
from datetime import datetime
import logging, json
logging.basicConfig(
    filename='dnsCompare_{}.log'.format(datetime.now().strftime("%Y%m%d")),
    filemode='a', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s, %(levelname)s, %(message)s')

mmlResult = "MML_Task_Result_DNS_TAC30D_20220422_134145.txt"

def getNeName(str):
    return str.split(':')[1].strip()

def main():
    logging.debug(f"Started")
    with open(mmlResult, 'r') as raw_mml:
        json_dict = {}
        neName = ''
        resrec = []
        for line in raw_mml.readlines():
            line = line.strip()

            if line.startswith('NE :'):
                # commit current NE if any
                if neName:
                    f_resrec = resrec
                    json_dict[neName] = f_resrec
                    logging.debug(f"Committing {neName}")
                    neName = ''
                    resrec = []
                neName = getNeName(line)
                resrec = []

            if line.startswith('TAC-'):
                resrec.append(line)
        # commit last NE
        if neName:
            f_resrec = resrec
            json_dict[neName] = f_resrec
            logging.debug(f"Committing {neName}")
            neName = ''
            resrec = []

    #with open('dnsTac.json', 'w') as fp:
    #    json.dump(json_dict, fp)

    keys = list(json_dict.keys())
    if len(keys)>2:
        logging.warning(f"Warning: Too many loaded NE. (NE={len(keys)})")

    js0 = json_dict[keys[0]]
    js1 = json_dict[keys[1]]

    logging.debug(f"Comparing {keys[0]} on {keys[1]}")
    for item in js0:
        if item not in js1:
            logging.info(f"Info: {keys[1]} missing {item}")

    logging.debug(f"Comparing {keys[1]} on {keys[0]}")
    for item in js1:
        if item not in js0:
            logging.info(f"Info: {keys[0]} missing {item}")


if __name__ == "__main__":
    main()
    logging.debug(f"Finished")
