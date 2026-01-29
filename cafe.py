import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# ==============================
# CONFIGURACIÓN
# ==============================

Window.clearcolor = get_color_from_hex('#f5f5f5')

# ==============================
# PANTALLA DE INICIO
# ==============================

class InicioScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(40), spacing=dp(20))
        
        # Espacio superior
        layout.add_widget(BoxLayout(size_hint_y=None, height=dp(50)))
        
        # Logo
        logo_box = BoxLayout(orientation='vertical', 
                           spacing=dp(10),
                           size_hint_y=None,
                           height=dp(200))
        
        logo_icon = Label(
            text='💻☕',
            font_size='64sp',
            size_hint_y=None,
            height=dp(80)
        )
        
        title = Label(
            text='[b]CodeBrew Café[/b]\nMenú Digital',
            font_size='28sp',
            color=get_color_from_hex('#2c3e50'),
            markup=True,
            halign='center',
            size_hint_y=None,
            height=dp(60)
        )
        title.bind(size=title.setter('text_size'))
        
        subtitle = Label(
            text='Tecnología con sabor',
            font_size='16sp',
            color=get_color_from_hex('#7f8c8d'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        subtitle.bind(size=subtitle.setter('text_size'))
        
        logo_box.add_widget(logo_icon)
        logo_box.add_widget(title)
        logo_box.add_widget(subtitle)
        layout.add_widget(logo_box)
        
        # Espacio
        layout.add_widget(BoxLayout(size_hint_y=None, height=dp(30)))
        
        # Botón principal
        menu_btn = Button(
            text='VER MENÚ',
            font_size='20sp',
            size_hint=(0.8, None),
            height=dp(60),
            pos_hint={'center_x': 0.5},
            background_color=get_color_from_hex('#3498db'),
            background_normal='',
            color=get_color_from_hex('#ffffff'),
            bold=True
        )
        menu_btn.bind(on_press=self.ir_a_menu)
        layout.add_widget(menu_btn)
        
        # Espacio
        layout.add_widget(BoxLayout())
        
        # Footer
        footer = Label(
            text='v1.0 - Asignación Universitaria',
            font_size='12sp',
            color=get_color_from_hex('#95a5a6'),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(footer)
        
        self.add_widget(layout)
    
    def ir_a_menu(self, instance):
        self.manager.current = 'categorias'

# ==============================
# PANTALLA DE CATEGORÍAS
# ==============================

class CategoriasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=[dp(10), 0])
        
        with header.canvas.before:
            Color(rgba=get_color_from_hex('#2c3e50'))
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        
        def update_header(instance, value):
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        
        header.bind(pos=update_header, size=update_header)
        
        # Botón de regreso
        back_btn = Button(
            text='← Inicio',
            font_size='18sp',
            size_hint=(None, 1),
            width=dp(100),
            background_color=get_color_from_hex('#34495e'),
            background_normal='',
            color=get_color_from_hex('#ffffff')
        )
        back_btn.bind(on_press=self.volver_inicio)
        
        # Título
        title = Label(
            text='[b]CATEGORÍAS[/b]',
            font_size='22sp',
            color=get_color_from_hex("#181717"),
            markup=True
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(BoxLayout())  # Espacio
        
        # ScrollView para categorías
        scroll = ScrollView()
        
        self.categories_grid = GridLayout(
            cols=1,
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(20), dp(20)]
        )
        self.categories_grid.bind(minimum_height=self.categories_grid.setter('height'))
        
        scroll.add_widget(self.categories_grid)
        
        # Agregar todo al layout principal
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Cargar categorías cuando se entra a la pantalla
        self.cargar_categorias()
    
    def cargar_categorias(self):
        self.categories_grid.clear_widgets()
        
        try:
            with open('menu.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Colores para cada categoría
            colors = [
                get_color_from_hex('#3498db'),  # Azul
                get_color_from_hex('#e74c3c'),  # Rojo
                get_color_from_hex('#9b59b6'),  # Púrpura
            ]
            
            # Íconos para categorías
            icons = ['🥤', '🍕', '🍰']
            
            for i, categoria in enumerate(datos['categorias']):
                # Crear botón para la categoría
                btn = Button(
                    text=f'{icons[i] if i < len(icons) else "⭐"} {categoria["nombre"]}\n[size=14]{categoria["descripcion"]}[/size]',
                    size_hint_y=None,
                    height=dp(100),
                    markup=True,
                    background_color=colors[i] if i < len(colors) else get_color_from_hex('#2c3e50'),
                    background_normal='',
                    color=get_color_from_hex('#ffffff'),
                    halign='center',
                    valign='middle'
                )
                
                # Centrar el texto
                btn.bind(size=lambda btn, size: setattr(btn, 'text_size', (size[0] - dp(20), None)))
                
                # Guardar el ID de la categoría
                btn.categoria_id = categoria['id']
                
                # Asignar evento
                btn.bind(on_press=self.ver_productos)
                
                self.categories_grid.add_widget(btn)
        
        except FileNotFoundError:
            error_label = Label(
                text='Error: No se encontró menu.json',
                color=get_color_from_hex('#ff0000'),
                size_hint_y=None,
                height=dp(50)
            )
            self.categories_grid.add_widget(error_label)
        
        except Exception as e:
            error_label = Label(
                text=f'Error: {str(e)}',
                color=get_color_from_hex('#ff0000'),
                size_hint_y=None,
                height=dp(50)
            )
            self.categories_grid.add_widget(error_label)
    
    def ver_productos(self, instance):
        # Guardar la categoría seleccionada
        app = App.get_running_app()
        app.categoria_actual = instance.categoria_id
        
        # Ir a productos
        self.manager.current = 'productos'
    
    def volver_inicio(self, instance):
        self.manager.current = 'inicio'

# ==============================
# PANTALLA DE PRODUCTOS
# ==============================

class ProductosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=None, height=dp(70), padding=[dp(10), 0])
        
        with header.canvas.before:
            Color(rgba=get_color_from_hex('#2c3e50'))
            self.header_rect = Rectangle(pos=header.pos, size=header.size)
        
        def update_header(instance, value):
            self.header_rect.pos = instance.pos
            self.header_rect.size = instance.size
        
        header.bind(pos=update_header, size=update_header)
        
        # Botón de regreso
        back_btn = Button(
            text='← Categorías',
            font_size='18sp',
            size_hint=(None, 1),
            width=dp(120),
            background_color=get_color_from_hex('#34495e'),
            background_normal='',
            color=get_color_from_hex('#ffffff')
        )
        back_btn.bind(on_press=self.volver_categorias)
        
        # Título (se actualizará dinámicamente)
        self.title_label = Label(
            text='PRODUCTOS',
            font_size='22sp',
            color=get_color_from_hex('#ffffff'),
            markup=True
        )
        
        header.add_widget(back_btn)
        header.add_widget(self.title_label)
        header.add_widget(BoxLayout())  # Espacio
        
        # ScrollView para productos
        scroll = ScrollView()
        
        self.products_grid = GridLayout(
            cols=1,
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(15), dp(15)]
        )
        self.products_grid.bind(minimum_height=self.products_grid.setter('height'))
        
        scroll.add_widget(self.products_grid)
        
        # Agregar todo al layout principal
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Cargar productos cuando se entra a la pantalla
        self.cargar_productos()
    
    def cargar_productos(self):
        self.products_grid.clear_widgets()
        
        try:
            with open('menu.json', 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            app = App.get_running_app()
            categoria_id = getattr(app, 'categoria_actual', 1)
            
            # Buscar el nombre de la categoría
            categoria_nombre = "Productos"
            for cat in datos['categorias']:
                if cat['id'] == categoria_id:
                    categoria_nombre = cat['nombre']
                    self.title_label.text = f'[b]{categoria_nombre}[/b]'
                    break
            
            # Filtrar productos por categoría
            productos_filtrados = []
            for producto in datos['productos']:
                if producto['categoria_id'] == categoria_id:
                    productos_filtrados.append(producto)
            
            if not productos_filtrados:
                self.mostrar_vacio()
                return
            
            # Crear una tarjeta para cada producto
            for producto in productos_filtrados:
                card = self.crear_card_producto(producto)
                self.products_grid.add_widget(card)
        
        except FileNotFoundError:
            self.mostrar_error("No se encontró menu.json")
        
        except Exception as e:
            self.mostrar_error(str(e))
    
    def crear_card_producto(self, producto):
        """Crea una tarjeta visual para un producto"""
        # Layout principal de la tarjeta
        card = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(120),
            padding=dp(15),
            spacing=dp(15)
        )
        
        # Fondo de la tarjeta
        with card.canvas.before:
            Color(rgba=get_color_from_hex('#ffffff'))
            self.card_bg = RoundedRectangle(
                pos=card.pos,
                size=card.size,
                radius=[dp(10),]
            )
        
        # Actualizar posición del fondo cuando la tarjeta se mueva
        def update_card_bg(instance, value):
            self.card_bg.pos = instance.pos
            self.card_bg.size = instance.size
        
        card.bind(pos=update_card_bg, size=update_card_bg)
        
        # Columna izquierda: Ícono
        icon_col = BoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1)
        )
        
        icon_label = Label(
            text=producto.get('icono', '☕'),
            font_size='32sp',
            halign='center',
            valign='middle'
        )
        icon_label.bind(size=icon_label.setter('text_size'))
        
        icon_col.add_widget(icon_label)
        
        # Columna central: Información
        info_col = BoxLayout(
            orientation='vertical',
            size_hint=(0.6, 1),
            spacing=dp(5)
        )
        
        # Nombre del producto
        name_label = Label(
            text=f'[b]{producto["nombre"]}[/b]',
            font_size='18sp',
            color=get_color_from_hex('#2c3e50'),
            markup=True,
            halign='left',
            size_hint_y=None,
            height=dp(30)
        )
        name_label.bind(size=name_label.setter('text_size'))
        
        # Descripción
        desc_label = Label(
            text=producto['descripcion'],
            font_size='14sp',
            color=get_color_from_hex('#7f8c8d'),
            halign='left',
            size_hint_y=None,
            height=dp(50)
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        
        info_col.add_widget(name_label)
        info_col.add_widget(desc_label)
        
        # Columna derecha: Precio
        price_col = BoxLayout(
            orientation='vertical',
            size_hint=(0.2, 1)
        )
        
        price_label = Label(
            text=f'[b]L{producto["precio"]:.2f}[/b]',
            font_size='20sp',
            color=get_color_from_hex('#27ae60'),
            markup=True,
            halign='center',
            valign='middle'
        )
        
        price_col.add_widget(price_label)
        
        # Agregar todas las columnas a la tarjeta
        card.add_widget(icon_col)
        card.add_widget(info_col)
        card.add_widget(price_col)
        
        return card
    
    def mostrar_vacio(self):
        """Muestra un mensaje cuando no hay productos"""
        empty_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            padding=dp(30)
        )
        
        icon_label = Label(
            text='📭',
            font_size='48sp',
            size_hint_y=None,
            height=dp(60)
        )
        
        message_label = Label(
            text='[b]No hay productos[/b]\n\nEsta categoría está vacía',
            font_size='16sp',
            color=get_color_from_hex('#7f8c8d'),
            markup=True,
            halign='center'
        )
        message_label.bind(size=message_label.setter('text_size'))
        
        empty_box.add_widget(icon_label)
        empty_box.add_widget(message_label)
        
        self.products_grid.add_widget(empty_box)
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        error_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(150),
            padding=dp(20)
        )
        
        with error_box.canvas.before:
            Color(rgba=get_color_from_hex('#e74c3c'))
            Rectangle(pos=error_box.pos, size=error_box.size)
        
        error_label = Label(
            text=f'[b]Error[/b]\n{mensaje}',
            color=get_color_from_hex("#ffffff"),
            markup=True,
            halign='center'
        )
        error_label.bind(size=error_label.setter('text_size'))
        
        error_box.add_widget(error_label)
        self.products_grid.add_widget(error_box)
    
    def volver_categorias(self, instance):
        self.manager.current = 'categorias'

# ==============================
# APLICACIÓN PRINCIPAL
# ==============================

class MenuApp(App):
    def build(self):
        self.title = 'CodeBrew Café - Menú Digital'
        self.categoria_actual = 1
        
        sm = ScreenManager()
        sm.add_widget(InicioScreen(name='inicio'))
        sm.add_widget(CategoriasScreen(name='categorias'))
        sm.add_widget(ProductosScreen(name='productos'))
        
        return sm

if __name__ == '__main__':
    MenuApp().run()