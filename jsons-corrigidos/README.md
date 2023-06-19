Para evitar que problemas fossem obtidos durante a etapa de treinamento, imagens que contêm regiões sem rótulo definido foram removidas. Foi utilizado o script localizado em ```scripts/remove_void.py``` para resolver esse problema, através do seguinte código de comando:

```
python remove_void.py -t dados-redimensionados/
```

A nova pasta com os arquivos ```.json``` corrigidos foi renomeada para ```jsons-corrigidos/```.