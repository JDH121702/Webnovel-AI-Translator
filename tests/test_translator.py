import unittest
from unittest.mock import patch
from translator.gpt_translator import translate_text

class TestTranslator(unittest.TestCase):
    @patch('translator.gpt_translator.openai.ChatCompletion.create')
    def test_translate_text(self, mock_create):
        mock_create.return_value = {
            'choices': [{
                'message': {
                    'content': 'This is a translated text.'
                }
            }]
        }
        result = translate_text("Este es un texto en español.")
        self.assertEqual(result, "This is a translated text.")

if __name__ == '__main__':
    unittest.main()
