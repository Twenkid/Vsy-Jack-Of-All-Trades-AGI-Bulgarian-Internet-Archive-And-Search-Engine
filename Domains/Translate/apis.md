# APIs and models for Machine Translation
By Todor Arnaudov, 20.5.2024:

https://pypi.org/project/deep-translator/

https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-translate

I've worked a bit with this python library the google service for "Smarty 2" in late 3.2024 - early 4.2024 (but then other domains and work took the charge).
Google translate is free through this library, your IP etc. may get temporarily suspended after certain amount of requests, but then it comes back, if you use it reasonably, say a request in 2-3 seconds.
The max length is 5000 chars like with the online Google translate. 

Microsoft offers a free service for 2 million chars per month after registration and it is a powerful API with additional configurations, "dynamic dictionary", translation of whole documents or sets etc.
Tier T0. 
https://learn.microsoft.com/en-us/azure/ai-services/translator/service-limits#character-and-array-limits-per-request

https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-translate

https://learn.microsoft.com/en-us/azure/ai-services/translator/custom-translator/concepts/customization

https://learn.microsoft.com/en-us/azure/ai-services/translator/reference/v3-0-reference#authentication

https://learn.microsoft.com/en-us/azure/ai-services/translator/service-limits#character-and-array-limits-per-request


(I haven't investigated GT for advanced features, I guess they have them too.)

Whisper can also be used for translation, but from speech as a source, I couldn't find an out-of-the box way to by-pass that step.

However there's another free model by Meta called NLLB: No language left behind for 200 languages with various sizes from 600M to 3.3B, it's created in 2022.
It's designed for sentence translations, up to 500 tokens.

I have just tried it with the small size distilled, 600M params.

https://medium.com/@FaridSharaf/text-translation-using-nllb-and-huggingface-tutorial-7e789e0f7816

https://huggingface.co/facebook/nllb-200-distilled-600M

https://huggingface.co/facebook/nllb-200-3.3B

However it is slow even on the Tesla T4, not practical for bulk processing of large volumes of text, the online services seem better for that purpose.
