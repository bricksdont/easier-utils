# srt2via v 1.0.0
import sys, getopt
import srt as SRT
from html.parser import HTMLParser
import json
import time
import re
import copy
import csv

NEW_SENTENCE, INNER_SENTENCE, NONE = range(3)
VIA_PROJECT_JSON_TEMPLATE ='{"project":{"pid":"__VIA_PROJECT_ID__","rev":"__VIA_PROJECT_REV_ID__","rev_timestamp":"__VIA_PROJECT_REV_TIMESTAMP__","pname":"__VIA_PROJECT_NAME__","creator":"Content4All VIA Fork (Credits: http://www.robots.ox.ac.uk/~vgg/software/via)","created":-1,"vid_list":["1"]},"config":{"file":{"loc_prefix":{"1":"","2":"","3":"","4":""}},"ui":{"file_content_align":"center","file_metadata_editor_visible":true,"spatial_metadata_editor_visible":true,"spatial_region_label_attribute_id":"","gtimeline_container_height":"45"}},"attribute":{"1":{"aname":"Subtitle","anchor_id":"FILE1_Z2_XY0","type":1,"desc":"","options":{},"default_option_id":""}},"file":{"1":{"fid":"1","fname":"__VIA_VIDEO_NAME__","type":4,"loc":2,"src":"__VIA_VIDEO_URL__"}},"metadata":{"1_00000000":{"vid":"1","flg":0,"z":[-1,-1],"xy":[],"av":{"1":"__VIA_VIDEO_SUBTITLE__"}}},"view":{"1":{"fid_list":["1"]}}}'
parsed_data = ''

class HTMLP(HTMLParser):
    def handle_data(self, data):
        global parsed_data
        parsed_data += data.strip()
        if parsed_data.endswith('-') == False or parsed_data.endswith(' -') == True:
            parsed_data += ' '

def createProjectFile(project_name, video_url, srt_file_path, srt_file_encoding, output_folder):

    # read SRT
    input_subtitle_file = open(srt_file_path, 'r', encoding=srt_file_encoding)
    subtitle_generator = SRT.parse(input_subtitle_file)
    subtitles = list(subtitle_generator)

    html_parser = HTMLP()
    sentences = []
    status = NEW_SENTENCE
    i = -1
    for subtitle in subtitles:

        # Get text from subtitles
        text = ''
        for line in subtitle.content.splitlines():
            global parsed_data
            parsed_data = ''
            html_parser.feed(line)
            text += parsed_data

        # Prepare text to be splitted
        text = text.strip()
        text = text.replace('."', '#".')
        text = text.replace('!"', '#"!')
        text = text.replace('?"', '#"?')
        text = text.replace('..."', '#"...')
        text = re.sub(R'([.;?!]{1,3}(?!\d))', R'\1\n', text)
        text = text.replace('#".', '."')
        text = text.replace('#"!', '!"')
        text = text.replace('#"?', '?"')
        text = text.replace('#"...', '..."')

        # Split text
        text_list = text.splitlines(True)
        text_list_len = len(text_list)

        # Create Sentences and match them with subtitle timestamps
        j = 0
        while (j < text_list_len):

            # 0. START TIMESTAMP
            if status == NEW_SENTENCE:
                i += 1
                sentences.append([subtitle.start.total_seconds(), '', -1])
                status = NONE

            if status == INNER_SENTENCE:
                i += 1
                sentences.append([sentences[i-1][2], '', -1])
                status = NONE

            # 1. SENTENCE
            sentences[i][1] += text_list[j].replace('\n', '')
            if sentences[i][1].endswith('-') == False or sentences[i][1].endswith(' -') == True:
                sentences[i][1] += ' '

            # 2. END TIMESTAMP
            sentences[i][2] = subtitle.end.total_seconds()

            if '\n' in text_list[j]:

                status = NEW_SENTENCE

                if text_list_len != 1 and j != text_list_len-1:
                    subtitle_duration = subtitle.end.total_seconds() - subtitle.start.total_seconds()
                    sentences[i][2] = subtitle.start.total_seconds() + (subtitle_duration * ( (j+1) / text_list_len ))
                    status = INNER_SENTENCE

            j += 1

    # prepare VIA project from template
    via_project_dict = json.loads(VIA_PROJECT_JSON_TEMPLATE)

    via_project_dict["project"]["created"] = int(round(time.time() * 1000))
    via_project_dict["project"]["pname"] = project_name
    via_project_dict["file"]["1"]["fname"] = video_url
    via_project_dict["file"]["1"]["src"] = video_url
    default_template = copy.deepcopy(via_project_dict["metadata"]["1_00000000"])

    # Put Sentences and their timestamps in VIA Project
    k = 0
    for sentence in sentences:
        template = copy.deepcopy(default_template)
        template["z"][0] = sentence[0]
        template["z"][1] = sentence[2]
        template["av"]["1"] = "[" + format(k, '04d') + "] " + sentence[1].strip()

        # format(10, '08d')
        metadata_id = "1_" + format(k, '08d')
        via_project_dict["metadata"].update({metadata_id:template})
        k += 1

    # Write VIA Project file
    with open(output_folder + '/' + project_name + '.json', "w", encoding='UTF-8') as write_file:
        json.dump(via_project_dict, write_file, indent=2)

def main(argv):

    input_csv_path = ''
    output_folder = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=", "ofolder="])
    except getopt.GetoptError:
        print ('srt2via.py -i <input_csv_path> -o <output_folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('srt2via.py -i <input_csv_path> -o <output_folder>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_csv_path = arg
        elif opt in ("-o", "--ofolder"):
            output_folder = arg

    # read CSV
    with open(input_csv_path, mode='r') as csv_file:
        input_csv = csv.DictReader(csv_file)
        for row in input_csv:
            createProjectFile(row["project_name"], row["video_url"], row["srt_file_path"], row["srt_file_encoding"], output_folder)

if __name__ == "__main__":
    main(sys.argv[1:])
