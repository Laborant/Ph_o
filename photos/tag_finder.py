from os.path import join

import json
import shutil
import os


class TagFinder:

    def __init__(self):
        self.path_from = "/home/ubuntu/Загрузки/sport/3"
        self.path_to = "/home/ubuntu/Загрузки/sport/select_photo"

    @staticmethod
    def check_exist_path(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def save_json(data, json_name='tags'):
        """
        Saving json of ensemble faces data
        :param data:
        :param json_name:
        """
        with open(json_name + '.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def read_json(json_name):
        """
        Read json of ensemble faces data
        :param json_name:
        :return: json
        """
        with open(json_name, "r") as f:
            return json.load(f)

    @staticmethod
    def get_idx_tag(_json, find_tag):
        """
        :return:
        """
        return next((idx for (idx, val) in enumerate(_json["tags"]) if val["tag"] == find_tag), None)

    def find_tag_copy_img(self, find_tag):
        """
        :param find_tag:
        :return:
        """
        _json = self.read_json('tags_3.json')
        idx = self.get_idx_tag(_json, find_tag)
        if idx is None:
            print("Images is not finded")
        else:
            images_list = _json["tags"][idx]["images"]
            print(f"Finded images: {images_list}")
            self.check_exist_path(self.path_to)
            for img_n in images_list:
                try:
                    shutil.copy(join(self.path_from, img_n), join(self.path_to, img_n))
                except Exception as err:
                    print(err)
            print("All images have been copied successfully")


if __name__ == '__main__':

    tagFinder = TagFinder()
    tag_id = '1060'
    tagFinder.find_tag_copy_img(tag_id)
