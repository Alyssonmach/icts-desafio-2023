Utilizando a sugestão de divisão dos dados, armazenados em arquivos ```.txt``` em estratos de treinamento, validação e teste, em uma aproximação respectiva de 70%, 10% e 20%, respectivamente, localizada na pasta ```guia-estratificacao-arquivos/```, o script ```scripts/split_jsons.py``` foi utilizado para resolver esse problema. O seguinte código de comando foi utilizado:

```
python split_jsons.py -t jsons-corrigidos/
```

A nova pasta com os arquivos ```.json``` estratificados foi renomeada para ```jsons-estratificados/```.