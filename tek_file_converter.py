import yaml
import json
import os

ERROR_FAILED_TO_LOAD_FILE = -4
ERROR_FAILED_TO_WRITE_FILE = -3
WARNING_FILE_NOT_FOUND = -2
WARNING_UNSUPORTED_FORMAT = -1
SUCCESS = 0

class TekConverter:

    def convert(self, input:str, output:str) -> int:

        settings = dict()

        if os.path.exists(input):

            # LOADING INPUT FILE
            if ".tek" in input:
                if not self.__load_tek(settings, input):
                    return ERROR_FAILED_TO_LOAD_FILE
            elif ".json" in input:
                if not self.__load_json(settings, input):
                    return ERROR_FAILED_TO_LOAD_FILE
            elif ".yaml" in input:
                if not self.__load_yaml(settings, input):
                    return ERROR_FAILED_TO_LOAD_FILE
            else:
                return WARNING_UNSUPORTED_FORMAT

            # WRITING OUTPUT FILE
            if ".tek" in output:
                if not self.__write_tek(settings, output):
                    return ERROR_FAILED_TO_WRITE_FILE
            elif ".json" in output:
                if not self.__write_json(settings, output):
                    return ERROR_FAILED_TO_WRITE_FILE
            elif ".yaml" in output:
                if not self.__write_yaml(settings, output):
                    return ERROR_FAILED_TO_WRITE_FILE
            else:
                return WARNING_UNSUPORTED_FORMAT
            
            return SUCCESS
        
        else:

            return WARNING_FILE_NOT_FOUND

    def __write_yaml(self, settings:dict, output:str) -> bool:

        try:

            with open(output, 'w') as file:
                yaml.dump(settings, file, sort_keys=False, allow_unicode=True)

            return True

        except:

            return False

    def __write_json(self, settings:dict, output:str) -> bool:

        try:

            with open(output, 'w') as file:
                json.dump(settings, file, indent=4)

            return True

        except:

            return False

    def __write_tek(self, settings:dict, output:str) -> bool:

        try:

            with open(output, "w") as file:
                for header in settings:
                    for index in settings[header]:
                        description = settings[header][index]["description"]
                        description = (" ; " if description != "" else "") + description
                        file.write("<" + header + "> " + (index[1:] if header != "chip" else "") + description + "\n")
                        for key in settings[header][index]:
                            if key != "description":
                                file.write(" " * 4 + (key if not "eddy" in key else "eddy") + " = " + settings[header][index][key] + "\n")

                        file.write("\n")

            return True
        
        except:

            return False

    def __load_yaml(self, settings:dict, input:str) -> bool:

        try:

            with open(input, "r") as file:
                settings.update(yaml.load(file, Loader=yaml.FullLoader))
            return True
        
        except:

            return False

    def __load_json(self, settings:dict, input:str):

        try:

            with open(input, "r") as file:
                settings.update(json.load(file))
            return True
        
        except:

            return False

    def __load_tek(self, settings:dict, input:str) -> bool:

        try:

            with open(input, "r") as file:
                header = ""
                index = ""
                for line in file:
                    line = line.strip()
                    if line:
                        if "<" == line[0] and ">" in line:

                            # SEPARATING HEADER_INDEX AND DESCRIPTION IF DESCRIPTION EXISTS
                            splited_line_content = line.split(";")

                            if len(splited_line_content) == 2: # DESCRIPTION EXISTS
                                header_index, description = [splited_line_content[0].strip(), splited_line_content[1].strip()]
                            else: # DESCRIPTION DOES NOT EXISTS
                                header_index, description = [splited_line_content[0].strip(), ""]

                            # SEPARATING HEADER AND INDEX
                            splited_header_index = header_index.split(" ")

                            # CLEANING EMPTY SPACES IN LIST
                            splited_header_index = [item for item in splited_header_index if item]

                            if len(splited_header_index) == 1: # INDEX DOES NOT EXISTS
                                header, index = [splited_header_index[0].replace("<", "").replace(">", ""), "0"]
                            else: # INDEX EXISTS
                                header, index = [splited_header_index[0].replace("<", "").replace(">", ""), splited_header_index[1]]
                            
                            # IF THE HEADER IS NOT INCLUDED IN SETTINGS CREATE A NEW KEY
                            if header not in settings:
                                settings[header] = {}
                            
                            index = header[0].upper() + index

                            # ADD THE INDEX AND THE DESCRIPTION
                            settings[header][index] = {"description": description}

                        elif ";" != line[0]:
                            # STORING CHIP, LAYER, METAL OR VIA PARAMS
                            key = line.split("=")[0].strip()
                            value = line.split("=")[-1].split(";")[0].strip()
                            key = "eddy1" if key == "eddy" and not settings[header][index].get("eddy1") else "eddy2" if key == "eddy" and settings[header][index].get("eddy1") else key
                            settings[header][index][key] = value

            return True
        
        except:

            return False
