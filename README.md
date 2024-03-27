# Bipartite-graph

## Graf

### Tworzenie obiektu klasy Graph

Wierzchołki liczone są od 0.

```
n = 5  # liczba wierzchołków na jednym boku
edges = [(2,3), (1,4), (0,3)]  # krawędzie grafu (<lewy bok>, <prawy bok>)
graph = Graph(n, edges)
```

### Zmiana krawędzi grafu w istniejącym grafie

```
edges = [(2,2), (0,4), (1,1)]  # nowe krawędzie
graph.set_edges(edges)
```

### Obliczanie pól wielokątów poziomów parzystych i nieparzystych

Poziomy grafu liczone są tak jak w pythonie - od zera. Jako pierwsze zwracane jest pole poziomów parzystych, jako drugie - nieparzystych. `check_if_sums_up_to_square` sprawdza, czy podane pola sumują się do pola kwadratu, który powstał z grafu.

```
area_0, area_1 = graph.get_area_of_polys()
is_area_ok = graph.check_if_sums_up_to_square(area_0, area_1)
```


## Rysowanie

### Rysowanie grafu

Dostępne są następujące opcje rysowania grafu
- edges: true|false - rysowanie krawędzi grafu;
- intersections: true|false - rysowanie punktów przecięcia;
- polygons: true|false - wypełnianie wielokątów kolorami;
- frame: true|false - rysowanie obramowania grafu (boków kwadratu, który powstaje).

Domyślnie rysowne są tylko wierzchołki (których nie da się wyłączyć). Do narysowania grafu użyto `matplotlib`.

```
plot = graph.draw(edges=True, intersections=True, polygons=True, frame=True)
plot.show()
```

### Zmiana opcji rysowania grafu

W pliku settings.py można zmienić opcje rysowania grafu. Nazwy słowników muszą pozostać niezmienione, wszelkie opcje powinny mieć format

```
example_dict = {
  "<matplotlib drawing option>": <value>,
}
```
