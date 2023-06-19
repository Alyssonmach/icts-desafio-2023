O dataset original foi obtido através do Google Drive, disponibilizado pelos criadores no GitHub, na qual o mesmo pode ser obtidos [clicando aqui](https://drive.google.com/uc?export=download&confirm=no_antivirus&id=1Yz59yXCiPKS0_X4K3x9mW22NLnxjvrr0). Esse dataset foi adicionada a pasta ```dataset-original```. 

Em seguida, o script localizado em ```scripts/resize_image_and_annotation.py``` foi modificado para que fosse possível redimensionar as imagens do dataset para um tamanho de 640x360.   

A partir do script ```scripts/resize_image_and_annotation.py```, foi utilizado o seguinte código na linha de comando para que uma nova pasta fosse gerada com os códigos redimensionados:

```
python resize_image_and_annotation-final.py -t dataset-original/
```

A nova pasta com as imagens redimensionadas foi renomeada para ```dados-redimensionados/```.
