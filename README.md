# Calculadora Cientifica Python

Este proyecto es una **calculadora en Python** que funciona en consola y pretende incluir de **aritmética, álgebra lineal, cálculo, gráficas de funciones, etc.** 

Fue diseñado como un ejercicio de **colaboración con Git y GitHub**, donde cada grupo de estudiantes aporta un módulo matemático distinto.

---

## Objetivos del proyecto

* Practicar el uso de **Git y GitHub** en un flujo de trabajo colaborativo.
* Desarrollar código modular en **Python**.
* Implementar operaciones matemáticas básicas y avanzadas.
* Integrar todo en una aplicación de consola con menú interactivo.

---

## Estructura del repositorio

```
CalculadoraCientificaPython/
├── modulos/
├───└── aritmeticas.py
├── requirements.txt
├── main.py
└── README.md
```

---

## ▶️ Cómo ejecutar el programa

1. Clona el repositorio

   ```bash
   git clone https://github.com/usuario/CalculadoraCientificaPython.git
   cd CalculadoraCientificaPython
   ```
2. Crear y activar un entorno virtual  
    En Windows
	```
	python -m venv venv
	venv\Scripts\activate
	```  
	En Linux/MacOS
	```
	python3 -m venv venv
	source venv/bin/activate	
	```
3. Instalar las dependencias desde requirements.txt
	```
	pip install -r requirements.txt
	```
4. Ejecuta el archivo principal

   ```bash
   python main.py
   ```

---

## Flujo de trabajo con Git

1. **Clonar** el repositorio.
2. Crear una **rama nueva** para tu módulo:

   ```bash
   git checkout -b mi-modulo
   ```
3. Agregar tus cambios y hacer commit:

   ```bash
   git add .
   git commit -m "Agrego módulo de ..."
   ```
4. Subir tu rama al repositorio remoto:

   ```bash
   git push origin mi-modulo
   ```
5. Crear un **Pull Request** en GitHub para integrar tu aporte.


## 👥 Colaboradores

Este proyecto es desarrollado por estudiantes de la Universidad Nacional Rosario Castellanos Campus Coyoacan como práctica de **matemáticas aplicadas y control de versiones con Git**.
