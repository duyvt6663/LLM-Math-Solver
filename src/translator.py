import googletrans

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect

dict_map = {
    "òa": "oà",
    "Òa": "Oà",
    "ÒA": "OÀ",
    "óa": "oá",
    "Óa": "Oá",
    "ÓA": "OÁ",
    "ỏa": "oả",
    "Ỏa": "Oả",
    "ỎA": "OẢ",
    "õa": "oã",
    "Õa": "Oã",
    "ÕA": "OÃ",
    "ọa": "oạ",
    "Ọa": "Oạ",
    "ỌA": "OẠ",
    "òe": "oè",
    "Òe": "Oè",
    "ÒE": "OÈ",
    "óe": "oé",
    "Óe": "Oé",
    "ÓE": "OÉ",
    "ỏe": "oẻ",
    "Ỏe": "Oẻ",
    "ỎE": "OẺ",
    "õe": "oẽ",
    "Õe": "Oẽ",
    "ÕE": "OẼ",
    "ọe": "oẹ",
    "Ọe": "Oẹ",
    "ỌE": "OẸ",
    "ùy": "uỳ",
    "Ùy": "Uỳ",
    "ÙY": "UỲ",
    "úy": "uý",
    "Úy": "Uý",
    "ÚY": "UÝ",
    "ủy": "uỷ",
    "Ủy": "Uỷ",
    "ỦY": "UỶ",
    "ũy": "uỹ",
    "Ũy": "Uỹ",
    "ŨY": "UỸ",
    "ụy": "uỵ",
    "Ụy": "Uỵ",
    "ỤY": "UỴ",
}


class Translation:
    def __init__(self, from_lang="vi", to_lang="en", mode="ggtrans"):
        # The class Translation is a wrapper for the two translation libraries, googletrans and translate.
        print(mode)
        self.__mode = mode
        self.__from_lang = from_lang
        self.__to_lang = to_lang

        if mode == "ggtrans":
            self.translator = googletrans.Translator()
        # elif mode in 'translate':
        #     self.translator = translate.Translator(from_lang=from_lang,to_lang=to_lang)
        elif mode == "mbart50":
            raise NotImplementedError
        elif mode == "vi2en":
            assert from_lang == "vi" and to_lang == "en"
            self.__tokenizer = AutoTokenizer.from_pretrained(
                "vinai/vinai-translate-vi2en", src_lang="vi_VN"
            )
            self.__model = AutoModelForSeq2SeqLM.from_pretrained(
                "vinai/vinai-translate-vi2en"
            )
        elif mode == "w2w":
            pass

    def preprocessing(self, text):
        """
        It takes a string as input, and returns a string with all the letters in lowercase
        :param text: The text to be processed
        :return: The text is being returned in lowercase.
        """
        return text.lower()

    def __call__(self, text):
        """
        The function takes in a text and preprocesses it before translation
        :param text: The text to be translated
        :return: The translated text.
        """
        if self.__mode == "ggtrans":
            text = self.preprocessing(str(text))
            # print(text)
            return (
                self.translator.translate(text)
                if self.__mode in "translate"
                else self.translator.translate(text, dest=self.__to_lang).text
            )
        elif self.__mode == "mbart50":
            raise NotImplementedError
        elif self.__mode == "vi2en":
            for i, j in dict_map.items():
                text = text.replace(i, j)
            input_ids = self.__tokenizer(text, return_tensors="pt").input_ids
            output_ids = self.__model.generate(
                input_ids,
                decoder_start_token_id=self.__tokenizer.lang_code_to_id["en_XX"],
                num_return_sequences=1,
                num_beams=5,
                early_stopping=True,
            )
            en_text = self.__tokenizer.batch_decode(
                output_ids, skip_special_tokens=True
            )
            en_text = " ".join(en_text)
            return en_text
        elif self.__mode == "w2w":
            return self.__translate_w2w(text)

    def __translate_w2w(self, text):
        raise NotImplementedError


def detect_lang(text):
    try:
        lang = detect(text)
    except:
        lang = None
    return lang
