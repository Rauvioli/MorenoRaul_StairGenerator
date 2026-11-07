import math
import maya.cmds as cmds
from PySide6 import QtWidgets, QtCore

def stairs(num_of_steps=12, step_width=2.0, step_height=0.4, step_depth=0.8, 
                  stair_type="Spiral", radius=4.0, spiral_angle=15.0):
    
    try:
        stair_grp = cmds.group(empty=True, name=f"{stair_type.lower()}_stairs_grp")
        
        first_step = cmds.polyCube(width=step_width, height=step_height, depth=step_depth, name="stair_step_1")[0]
        cmds.parent(first_step, stair_grp)
        
        cmds.xform(first_step, piv=[0, 0, step_depth / 2.0], relative=True)
        
        if stair_type == "Straight":
            cmds.setAttr(f"{first_step}.translateY", step_height / 2.0)
        else:
            cmds.setAttr(f"{first_step}.translateX", radius)
            cmds.setAttr(f"{first_step}.translateY", step_height / 2.0)
        
        for bruh in range(1, num_of_steps):
            step = cmds.duplicate(first_step, name=f"stair_step_{bruh+1}")[0]
            
            if stair_type == "Straight":
                new_y = (step_height / 2.0) + (bruh * step_height)
                new_z = bruh * step_depth
                
                cmds.setAttr(f"{step}.translateY", new_y)
                cmds.setAttr(f"{step}.translateZ", new_z)
                
            elif stair_type == "Spiral":
                current_angle = bruh * spiral_angle
                rad_angle = math.radians(current_angle)
                
                X = radius * math.cos(rad_angle)
                Z = -radius * math.sin(rad_angle)
                Y = (step_height / 2.0) + (bruh * step_height)
                
                cmds.setAttr(f"{step}.translateX", X)
                cmds.setAttr(f"{step}.translateY", Y)
                cmds.setAttr(f"{step}.translateZ", Z)
                cmds.setAttr(f"{step}.rotateY", current_angle)
                
    finally:
        cmds.undoInfo(closeChunk=True)

class StairMenu(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Build-a-Stairs")
        self.resize(320, 300)
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.create_widgets()
        self.create_layout()
        self.connections() 

    def create_widgets(self):
        # Names for the stair options
        self.type_label = QtWidgets.QLabel("Stair Options:")
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Straight", "Spiral"])
        self.type_combo.setCurrentText("Spiral")

        # The dimensions for the steps
        self.count_label = QtWidgets.QLabel("How Many Steps?:")
        self.count_spin = QtWidgets.QSpinBox()
        self.count_spin.setRange(1, 200)
        self.count_spin.setValue(24)

        self.width_label = QtWidgets.QLabel("How Wide?:")
        self.width_spin = QtWidgets.QDoubleSpinBox()
        self.width_spin.setValue(2)

        self.height_label = QtWidgets.QLabel("How Tall?:")
        self.height_spin = QtWidgets.QDoubleSpinBox()
        self.height_spin.setValue(0.5)

        self.depth_label = QtWidgets.QLabel("How Looong?:")
        self.depth_spin = QtWidgets.QDoubleSpinBox()
        self.depth_spin.setValue(1.0)

        # Making spiral and options for its radius and rotation
        self.radius_label = QtWidgets.QLabel("Radius(for spiral!):")
        self.radius_spin = QtWidgets.QDoubleSpinBox()
        self.radius_spin.setValue(5.0)

        self.angle_label = QtWidgets.QLabel("Rotation Angle (for spiral!):")
        self.angle_spin = QtWidgets.QDoubleSpinBox()
        self.angle_spin.setRange(0.0, 180.0)
        self.angle_spin.setValue(15.0)

        # Building the button
        self.build_butt = QtWidgets.QPushButton("Build Stairs!")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QGridLayout()
        
        # Making menu background 
        form_layout.addWidget(self.type_label, 0, 0)
        form_layout.addWidget(self.type_combo, 0, 1)
        
        form_layout.addWidget(self.count_label, 1, 0)
        form_layout.addWidget(self.count_spin, 1, 1)
        
        form_layout.addWidget(self.width_label, 2, 0)
        form_layout.addWidget(self.width_spin, 2, 1)
        
        form_layout.addWidget(self.height_label, 3, 0)
        form_layout.addWidget(self.height_spin, 3, 1)
        
        form_layout.addWidget(self.depth_label, 4, 0)
        form_layout.addWidget(self.depth_spin, 4, 1)
        
        form_layout.addWidget(self.radius_label, 5, 0)
        form_layout.addWidget(self.radius_spin, 5, 1)
        
        form_layout.addWidget(self.angle_label, 6, 0)
        form_layout.addWidget(self.angle_spin, 6, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.build_butt)

    def connections(self):
        # making the buttons work
        self.build_butt.clicked.connect(self.on_build_clicked)


    def on_build_clicked(self):
        stairs(
            num_of_steps=self.count_spin.value(),
            step_width=self.width_spin.value(),
            step_height=self.height_spin.value(),
            step_depth=self.depth_spin.value(),
            stair_type=self.type_combo.currentText(),
            radius=self.radius_spin.value(),
            spiral_angle=self.angle_spin.value()
        )

stair_final = StairMenu()
stair_final.show()
