## Info 

本文所列的Prompt为最终使用的两个Prompt，如果需要查看更多Prompt的效果可以在结果中查看

The Prompt listed in this article is the final two used, if you need to see the effect of more Prompt can be seen in the results

## Chinise
### no repeat 
你会被提供语音识别后的短句,你的任务是在不引起更多错误的前提下纠正有把握纠正的同音或者读音相近的错别字，你必须给出推理的过程。

你应该按照下面的流程一步步的进行判断:(1)梳理句子的结构并且断句(2)判断句子是否有同音错别字(3)如果有错别字则将转化为有声调的汉语拼音(4)根据汉语拼音和上下文推断出候选的答案(5)选择上下文合理的答案,如果改变词的读音差别过大或者对答案没把握可以保持原句不变直接输出，答案用[]包裹,并且前面用<改>,<原>来表示是否修改

输入:他突然就干喔

断句：他 突然 就  干喔
推理:(1) "干喔" 有问题（(2)"干喔"的拼音是"gan1 wo3"(3)"gan1 wo3"的候选词有"干我"、"干窝","干呕"(4)最合适的选项为"干呕",但是"呕"和"喔"的读音分别为"ou3","wo",差别过大，不改变原句

结果:<原>[他突然就干喔]


输入:二零一八年还将举办第十四届世界短池游泳锦标赛

断句:二零一八年 还 将 举办 第十四届 世界 短池 游泳 锦标赛
推理:(1)句子没有语病，因此原样输出

结果:<原>[二零一八年还将举办第十四届世界短池游泳锦标赛]


输入:湖北荆州市安良百货公司事发首扶电梯已被关闭减修。
断句:湖北 荆州市 安良百货公司 事发 首扶电梯 已 被 关闭 减修。
推理:(1)句子有错别字，问题在"首扶","检修"(2)"首扶"的拼音是"shou3 fu2","减修"的拼音是"jian3 xiu1"(3)考虑上下文，"shou3 fu2"可能的候选词有"首次","手扶","首付",根据"jian3 xiu1"的拼音和上下文，三个候选答案可能是“检修”、“减修”、“建修”。(4)"手扶"、"检修"最符合上下文，并且"手扶"的读音为"shou3 fu2"和"首扶"一致，"检修"的读音为"jian3 xiu1"和"减修"一致，对答案有信心，因此纠正后的答案是："湖北荆州市安良百货公司事发手扶电梯已被关闭检修"，对答案持有信心，保留修改。

结果:<改>[湖北荆州市安良百货公司事发手扶电梯已被关闭检修]
'

### no split 
'
你会被提供语音识别后的短句,你的任务是把这些短句纠正为标准的没有错别字和语病的正确识别结果。通常而言错误是因为同音等等造成的.

你的判断流程应该是这样:(1)判断句子是否有语病，如果无语病就原样输出结束判断(2)如果有语病则将有语病的部分转化为有声调的汉语拼音进入(3)根据汉语拼音和上下文推断出三个候选的答案(4)选择上下文合理的答案,如果对答案没把握可以保持原句不变，直接输出，如果语句不通顺就继续判断,最多判断三次,结果通过<标志>[结果]的形式给出，标志可以是<原>,<改>

下面是一些例子：
他突然就干喔
(1) 句子有语病，问题在"干喔"(2)"干喔"的拼音是"gan4 wo1"(3)考虑上下文，"gan4"可能的候选词有"干"、"赶"、"敢"，"wo1"可能的候选词有"我"、"窝"、"喔"。(4)根据上下文，"敢我"最符合，因此纠正后的答案是:"他突然就敢我"，答案仍然有问题继续判断
(1) 句子有语病，问题在"干喔"(2)"干喔"的拼音是"gan4 wo1"(3)考虑上下文，"gan4 wo1"可能的候选词有"干呕"、"赶我"、"干我"。(4)根据上下文，"干呕"最符合，因此纠正后的答案是:"他突然就干呕"，语句没问题，结束判断
结果:<改>[他突然就干呕]

二零一八年还将举办第十四届世界短池游泳锦标赛
(1)句子没有语病，因此原样输出
结果:<原>[二零一八年还将举办第十四届世界短池游泳锦标赛]

湖北荆州市安良百货公司事发首扶电梯已被关闭减修。
(1)句子有语病，问题在"首扶","检修"(2)"首扶"的拼音是"shou3 fu2","减修"的拼音是"jian3 xiu1"(3)考虑上下文，"shou3 fu2"可能的候选词有"首次","手扶","首付",根据"jian3 xiu1"的拼音和上下文，三个候选答案可能是“检修”、“减修”、“建修”。(4)"手扶电梯"、"检修"最符合上下文，因此纠正后的答案是："湖北荆州市安良百货公司事发手扶电梯已被关闭检修"，语句没问题，结束判断
结果:<改>[湖北荆州市安良百货公司事发手扶电梯已被关闭检修]


'

### no flag(abandon)

'
你会被提供语音识别后的短句,你的任务是把这些短句纠正为标准的没有错别字和语病的正确识别结果。通常而言错误是因为同音等等造成的.

你的判断流程应该是这样:(1)判断句子是否有语病，如果无语病就原样输出结束判断(2)如果有语病则将有语病的部分转化为有声调的汉语拼音进入(3)根据汉语拼音和上下文推断出三个候选的答案(4)选择上下文合理的答案,如果对答案没把握可以保持原句不变，直接输出，如果语句不通顺就继续判断,最多判断三次

下面是一些例子：
他突然就干喔
(1) 句子有语病，问题在"干喔"(2)"干喔"的拼音是"gan4 wo1"(3)考虑上下文，"gan4"可能的候选词有"干"、"赶"、"敢"，"wo1"可能的候选词有"我"、"窝"、"喔"。(4)根据上下文，"敢我"最符合，因此纠正后的答案是:"他突然就敢我"，答案仍然有问题继续判断
(1) 句子有语病，问题在"干喔"(2)"干喔"的拼音是"gan4 wo1"(3)考虑上下文，"gan4 wo1"可能的候选词有"干呕"、"赶我"、"干我"。(4)根据上下文，"干呕"最符合，因此纠正后的答案是:"他突然就干呕"，语句没问题，结束判断
结果:[他突然就干呕]

二零一八年还将举办第十四届世界短池游泳锦标赛
(1)句子没有语病，因此原样输出
结果:[二零一八年还将举办第十四届世界短池游泳锦标赛]

湖北荆州市安良百货公司事发首扶电梯已被关闭减修。
(1)句子有语病，问题在"首扶","检修"(2)"首扶"的拼音是"shou3 fu2","减修"的拼音是"jian3 xiu1"(3)考虑上下文，"shou3 fu2"可能的候选词有"首次","手扶","首付",根据"jian3 xiu1"的拼音和上下文，三个候选答案可能是“检修”、“减修”、“建修”。(4)"手扶电梯"、"检修"最符合上下文，因此纠正后的答案是："湖北荆州市安良百货公司事发手扶电梯已被关闭检修"，语句没问题，结束判断
结果:[湖北荆州市安良百货公司事发手扶电梯已被关闭检修]

注意下面的事项:（1）任何和数字有关的内容都不应该被改变，比如“二零二三”这类数字不应该转写为“2023”，"四零零元"这类表示不应该被转写称为"四百元"，以及百分比等等(2)输入会有很多行，请分别对待每一行进行判断(3)你最多判断三次，三次后直接输出原文
'
## English

"
You will be provided with short speech recognition sentences, and your task is to correct these short sentences to a standard correct recognition result without typos and language errors. Usually, errors are due to homophones and so on.

To determine whether a sentence is defective, If there is no language disease, output the sentence or correct errors by thinking in the following way。

（1）Locate the position of the defective phrase in the sentence
（2）Give the pronunciation of the defective phrase
（3）Give multiple candidates  according to their pronunciation
（4）Select the appropriate candidates combined with the context

For the corrected sentence, you need to continue to determine whether there is a language problem. If you do not have confidence in the correction, then give up the correction. You can correct the sentence up to three times

Note:(1)Both input and output must be saved in all uppercase(2)(2)The answer is wrapped in [] and preceded by change#,#original# to indicate whether to change or not

Here are some examples,you need to give the reasoning process

Input:BECAUSE HE WANTED TO BREAD A NEW GENERATION OF BAKERS

Inference:The sentence has language problems, correct the sentence 
(1) the defective word is <bread>
(2) the pronunciation of <bread> is /bred/
(3) Given the candidate words <breed>-/briːd/, <bled>-/blɛd/, <brand>-/brænd/
(4) select <breed> according to the context, and the corrected sentence is none Speech disorders, output results

Result:#change#[BECAUSE HE WANTED TO BREED A NEW GENERATION OF BAKERS]

Input:DUE TO THEE THEIR PRAISE OF MAIDEN PURE OF TEEMING MOTHERHOOD

Inference:The sentence doesn't have language problems,output the origin sentence

Result:#original#[DUE TO THEE THEIR PRAISE OF MAIDEN PURE OF TEEMING MOTHERHOOD]

Input:ORGAN OF RUT NOT REASON IS THE LORD WHO FROM THE BODY POLITIC DOTH DRAIN LOST FOR HIMSELF INSTEAD OF TOIL AND PAIN LEAVING US LENA'S    CRICKETS ON DRY SWARD 

Inference: The sentence has language problems, correct the sentence.
(1) The defective phrase is <Lena's crickets>.
(2) The pronunciation of <Lena's crickets> is /ˈliːnəz ˈkrɪkɪts/.
(3) Given the candidate phrases: <lean as crickets> - /liːn əz ˈkrɪkɪts/, <lend us crickets> - /lɛnd ʌs ˈkrɪkɪts/, <Lenna's crickets> - /ˈlɛnəz ˈkrɪkɪts/.
(4) Select <lend us crickets> according to the context, and the corrected sentence is still has Speech disorders, abandoning this change and repeat inference.

Inference: The sentence has language problems, correct the sentence.
(1) The defective phrase is <Lena's crickets>.
(2) The pronunciation of <Lena's> is /ˈliːnəz/.
(3) Given the candidate phrases: <lean as> - /liːn æz/, <leaned as> - /liːnd æz/, <Lenas> - /ˈliːnəs/.
(4) Select <lean as> according to the context, as it fits better with the idea of being left in a lean or meager state. The corrected sentence is still not perfect, but there are no obvious language errors.

Result: #change#[ORGAN OF RUT NOT REASON IS THE LORD WHO FROM THE BODY POLITIC DOTH DRAIN LOST FOR HIMSELF INSTEAD OF TOIL AND PAIN LEAVING US LEAN AS CRICKETS ON DRY SWARD]
"