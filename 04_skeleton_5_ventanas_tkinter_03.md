# Documentación del Proyecto Integrador (tkinter MVP)

Aplicación de escritorio en Python con **tkinter** que consta de una ventana principal de navegación y cinco subventanas, cada una pensada para que la desarrolle un integrante del equipo y demuestre un conjunto distinto de widgets.

---

## 1. Resumen

| Elemento | Descripción |
|---|---|
| Lenguaje | Python 3 |
| Librería GUI | `tkinter` y `tkinter.ttk` (incluidas en la biblioteca estándar) |
| Otras librerías | `csv`, `pathlib` (estándar) |
| Punto de entrada | `src/app/main.py` |
| Editor | VS Code, con configuración de depuración en `.vscode/launch.json` |
| Patrón | Una función `open_win_*` por ventana, que crea un `tk.Toplevel` sobre la ventana raíz |

No hay dependencias externas: no se necesita `pip install`.

---

## 2. Estructura de carpetas

```
/src
  /app
    main.py        Ventana principal (menú de navegación)
    win_home.py    Ventana 1: Labels, Buttons, MessageBox
    win_form.py    Ventana 2: Entries, validación, FileDialog
    win_list.py    Ventana 3: Listbox con operaciones básicas
    win_table.py   Ventana 4: ttk.Treeview alimentada desde CSV
    win_canvas.py  Ventana 5: Canvas con dibujo básico
  /core
    helpers.py     Utilidades compartidas (opcional, sin uso actual)
  /data
    sample.csv     Datos de ejemplo para la tabla
  /tests           Reservada para pruebas
/.vscode
  launch.json      Configuración de ejecución/depuración
/docs              Documentación
```

> Nota: en el ZIP de la plantilla (`Sesion3.zip`), `data/` aparece en la raíz del repositorio, no dentro de `src/`. El código de `win_table.py` espera esa ubicación (ver sección 5.5).

---

## 3. Asignación de tareas

| Integrante | Archivo | Responsabilidad |
|---|---|---|
| A | `win_home.py` | Bienvenida + messagebox; coordina la integración |
| B | `win_form.py` | Formulario con validación y guardado en archivo |
| C | `win_list.py` | Listbox: agregar, eliminar, limpiar |
| D | `win_table.py` | Tabla Treeview que lee `data/sample.csv` |
| E | `win_canvas.py` | Dibujo básico con Canvas |

---

## 4. Arquitectura y flujo

```
main.py
  └─ tk.Tk() (root)
       ├─ Botón 1 → open_win_home(root)    → Toplevel
       ├─ Botón 2 → open_win_form(root)    → Toplevel
       ├─ Botón 3 → open_win_list(root)    → Toplevel
       ├─ Botón 4 → open_win_table(root)   → Toplevel
       ├─ Botón 5 → open_win_canvas(root)  → Toplevel
       └─ Salir   → root.destroy()
```

Ideas clave del diseño:

- **Una ventana por módulo.** Cada archivo expone una sola función pública `open_win_<nombre>(parent)`. Esto permite que cada integrante trabaje sin chocar con los demás.
- **`Toplevel` hijo de la raíz.** Solo existe un `Tk()`; las subventanas se cierran con `win.destroy()` sin terminar la aplicación.
- **Un solo `mainloop()`.** Se invoca únicamente en `main()`; las subventanas no lo necesitan.
- **Imports con `PYTHONPATH=src`.** `main.py` usa `from app.win_home import ...`, por lo que `src` debe estar en el path (lo resuelve `launch.json`).
- **`lambda` en los botones.** `command=lambda: open_win_home(root)` retrasa la llamada hasta el clic y permite pasar argumentos.

---

## 5. Explicación de cada archivo

### 5.1 `main.py` — Ventana principal

- Crea la raíz `tk.Tk()` con título y tamaño `420x340`.
- Dentro de un `ttk.Frame` con `padding=16` coloca un título (`ttk.Label`), cinco botones de navegación, un `ttk.Separator` y el botón **Salir**.
- Usa el gestor de geometría `pack` (`fill="x"` para que los botones ocupen todo el ancho).
- El bloque `if __name__ == "__main__": main()` evita que la app se ejecute al importar el módulo.

### 5.2 `win_home.py` — Ventana 1 (Labels, Buttons, MessageBox)

- Crea un `Toplevel` de `360x220`.
- Muestra dos etiquetas (título en negritas y texto de apoyo).
- El botón **Mostrar mensaje** lanza `messagebox.showinfo("Info", "¡Equipo listo!")`.
- El botón **Cerrar** destruye la ventana.

Conceptos que demuestra: `Label`, `Button`, `messagebox`, `pack`.

### 5.3 `win_form.py` — Ventana 2 (Entries, validación, FileDialog)

- Formulario con `grid`: etiquetas en la columna 0 y campos `ttk.Entry` en la columna 1 (**Nombre** y **Edad**).
- La función interna `validar_y_guardar()`:
  1. Lee y limpia (`strip()`) los valores.
  2. Si el nombre está vacío → `messagebox.showerror`.
  3. Si la edad no es `isdigit()` → `messagebox.showerror`.
  4. Abre `filedialog.asksaveasfilename` (extensión `.txt`).
  5. Si el usuario eligió ruta, escribe `Nombre: ...` y `Edad: ...` en UTF-8 y confirma con `showinfo`.
- Botones **Guardar** y **Cerrar** en la fila 3.

Conceptos que demuestra: `Entry`, validación de entrada, `filedialog`, escritura de archivos con `with open(...)`, funciones anidadas (closures) que acceden a los widgets.

### 5.4 `win_list.py` — Ventana 3 (Listbox + CRUD básico)

- `tk.Listbox` a la izquierda (ocupa 4 filas con `rowspan=4`); controles a la derecha.
- `columnconfigure/rowconfigure(weight=1)` hacen que la lista crezca al redimensionar la ventana.
- Funciones:
  - `agregar()`: inserta el texto del `Entry` al final (`"end"`) y limpia el campo; si está vacío muestra un aviso.
  - `eliminar()`: borra el elemento seleccionado (`curselection()[0]`).
  - `limpiar()`: vacía la lista completa (`delete(0, "end")`).

Conceptos que demuestra: `Listbox`, manejo de selección, `grid` con `sticky` y pesos de fila/columna.

### 5.5 `win_table.py` — Ventana 4 (Treeview + CSV)

- Define las columnas `("nombre", "valor1", "valor2")` y crea un `ttk.Treeview` con `show="headings"` (oculta la columna de árbol).
- Configura encabezados (`heading`) y columnas (`column`, ancho 120, centradas).
- Calcula la ruta del CSV de forma independiente del directorio de trabajo:
  `Path(__file__).resolve().parents[2] / "data" / "sample.csv"`
  (`parents[0]` = `app`, `[1]` = `src`, `[2]` = raíz del proyecto).
- Si el archivo no existe, muestra un aviso y termina.
- Si existe, lee con `csv.DictReader` e inserta cada fila con `tv.insert("", "end", values=(...))`.

`data/sample.csv`:

```csv
nombre,valor1,valor2
A,10,20
B,15,25
C,12,30
```

### 5.6 `win_canvas.py` — Ventana 5 (Canvas)

- Crea un `tk.Canvas` de `440x240` con fondo blanco.
- Dibuja primitivas: rectángulo (`create_rectangle`), óvalo con relleno (`create_oval`), línea (`create_line`) y texto (`create_text`).
- Las coordenadas son `(x1, y1, x2, y2)` con origen en la esquina superior izquierda.

Conceptos que demuestra: sistema de coordenadas del Canvas y creación de formas.

### 5.7 `.vscode/launch.json` — Ejecución y depuración

- Ejecuta `${workspaceFolder}/src/app/main.py`.
- `cwd` en la raíz del proyecto.
- `env.PYTHONPATH = ${workspaceFolder}/src`: hace que funcione `from app...`.
- `console: integratedTerminal` y `justMyCode: true` (no depura librerías).

---

## 6. Cómo ejecutar

**Desde VS Code:** abrir la carpeta del proyecto → *Run and Debug* (Ctrl+Shift+D) → seleccionar **Programa con PYTHONPATH=src** → F5.

**Desde terminal:**

```bash
# Windows (PowerShell)
$env:PYTHONPATH = "src"
python src/app/main.py

# macOS / Linux
PYTHONPATH=src python3 src/app/main.py
```

---

## 7. Observaciones y mejoras sugeridas

| # | Observación | Sugerencia |
|---|---|---|
| 1 | En `win_table.py`, si falta el CSV la función hace `return` antes de crear el botón **Cerrar** | Mover el botón antes de la lectura del archivo |
| 2 | Las ventanas no son modales: se pueden abrir varias copias de la misma | Usar `win.transient(parent)` y `win.grab_set()` |
| 3 | El "CRUD" de la lista solo cubre crear y eliminar | Agregar **Editar** (actualizar el elemento seleccionado) |
| 4 | `isdigit()` acepta algunos caracteres Unicode y no valida rangos | Usar `try: int(...)` y validar un rango (p. ej. 0–120) |
| 5 | `"type": "python"` en `launch.json` está obsoleto en versiones recientes de la extensión de Python | Cambiar a `"type": "debugpy"` |
| 6 | La fuente `Segoe UI` es de Windows; en macOS/Linux se sustituye por otra | Usar `TkDefaultFont` o una fuente multiplataforma |
| 7 | Las anotaciones `parent: tk.Tk` son estrictas, pero se acepta cualquier widget | Anotar como `tk.Misc` |
| 8 | `core/helpers.py` y `tests/` están vacíos | Mover ahí utilidades comunes (p. ej. ruta de `data/`) y agregar pruebas de la lógica de validación |
| 9 | Los valores leídos del CSV son cadenas | Convertir a `int`/`float` si se van a calcular |

---

## 8. Glosario rápido de widgets

| Widget | Uso en el proyecto |
|---|---|
| `Tk` | Ventana raíz |
| `Toplevel` | Subventanas |
| `ttk.Frame` | Contenedor con padding |
| `ttk.Label` / `ttk.Button` / `ttk.Entry` | Widgets temáticos básicos |
| `ttk.Separator` | Línea divisoria en el menú |
| `tk.Listbox` | Lista de elementos |
| `ttk.Treeview` | Tabla de datos |
| `tk.Canvas` | Dibujo 2D |
| `messagebox` | Diálogos de información, error y aviso |
| `filedialog` | Diálogo "Guardar como" |
