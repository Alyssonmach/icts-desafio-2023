O script ```scripts/split_jsons.py``` usa a divisão fixa da pasta ```guia-estratificacao-arquivos/``` (70% treino, 10% validação e 20% teste). Execute a partir da raiz do repositório:

```
python scripts/split_jsons.py -t jsons-corrigidos/ --output-dir jsons-estratificados/
```

O resultado contém as subpastas ```train_jsons/```, ```val_jsons/``` e ```test_jsons/```. Arquivos esperados que não existam na entrada são informados no terminal.
