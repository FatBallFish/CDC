import os
import jieba
import sys
from sklearn.feature_extraction.text import TfidfVectorizer


class TfIdf:

    def __init__(self, text: str = None, text_list: list = None, stop_words: set = None, user_dict_path: str = None):
        if text is None and text_list is None:
            raise
        elif text_list is not None:
            self.text_list = text_list
            print("text_list:", text_list)
        elif text is not None:
            self.text_list = [text]
            print("text:", text, "list:", self.text_list)
        if stop_words is None:
            self.STOP_WORDS = set()
        else:
            self.STOP_WORDS = stop_words
        if user_dict_path is not None:
            if os.path.exists(user_dict_path):
                try:
                    jieba.load_userdict(user_dict_path)
                except Exception as e:
                    pass

    def _cut(self, text: str) -> list:
        seg_list = jieba.cut(text)
        result = []
        for seg in seg_list:
            seg = ''.join(seg.split())
            if len(seg.strip()) >= 2 and seg.lower() not in self.STOP_WORDS:
                result.append(seg)
        return result

    def doJob(self, tfidfw: float = 0.3) -> list:
        corpus = []
        for text in self.text_list:
            result = self._cut(text)
            corpus.append(" ".join(result))

        vectorizer = TfidfVectorizer()  # 该类实现词向量化和Tf-idf权重计算
        tfidf = vectorizer.fit_transform(corpus)
        word = vectorizer.get_feature_names()
        weight = tfidf.toarray()
        ret_list = []
        for i in range(len(weight)):
            print('----------writing all the tf-idf in the ', i, "----------")
            result = {}
            sub_ret_list = []
            for j in range(len(word)):
                if weight[i][j] >= tfidfw:
                    result[word[j]] = weight[i][j]
            resultsort = sorted(result.items(), key=lambda item: item[1], reverse=True)
            for z in range(len(resultsort)):
                print(resultsort[z][0] + " " + str(resultsort[z][1]))
                sub_ret_list.append(resultsort[z][0])
            ret_list.append(sub_ret_list)
        return ret_list


if __name__ == '__main__':
    text_list = ["约会神器，春风费洛蒙固体香水（含礼盒装）", "宠物合金钢安全除菌指甲护理组合"]

    # tf = TfIdf(text=text_list[0])
    tf = TfIdf(text_list=text_list)
    ret_list = tf.doJob(0.3)
    print(ret_list)
