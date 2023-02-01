# robot4ws_description

## Create new body
Duplicate one of the existing body xacro file in ```/xacros/``` (e.g. ```rover_body.xacro```).
Duplicate the corresponding yaml file in ```/urdf/config/``` (e.g. ```body.yaml```).
### xacro configuration
Change the name of the object (e.g. "rover_leg" to "new_name")
```<xacro:macro name="rover_leg" params="name">```
Change the filename value:
```<xacro:property name="filename" value="$(find robot4ws_description)/urdf/config/leg.yaml"/>```

#### Link definition
In case you want to make the model parametric, you can add parameters to the xacro by adding parameters in the following line
```<xacro:macro name="rover_leg" params="name">``` to ```<xacro:macro name="rover_leg" params="name side">```
where, in this example, ```side``` stands for the side (left or right) of the rover.

When the xacro runs, the arguments defined in xacro:macro, i.e. ```name``` and ```side```, will be used to define the name of the urfd descriptor. This happens at line:
```<link name="${name}_leg_${side}">```

It then extracts the required information. The following line gets data from the ```body_config``` property. These are in the ```inertial``` key which is in the ```body``` key. This property was defined at the beginning, and it itself gets data from the yaml file.
```<xacro:property name="data" value="${body_config['body']['inertial']}"/>```

In the same way, the other parameters are extracted and assigned to the data structure ```inertial```:

```<inertial>```
```     <xacro:property name="data" value="${body_config['body']['inertial']}"/>```
```     <mass value="${data['mass']}"/>```
```     <origin xyz="${data['origin']['position']['x']} ${data['origin']['position']['y']} ${data['origin']['position']['z']}" rpy="${data['origin']['orientation']['roll']} ${data['origin']['orientation']['pitch']} ${data['origin']['orientation']['yaw']}"/>```
```     <inertia ixx="1.71402" ixy="0.0" ixz="0.0" iyy="0.8856" iyz="0.0" izz="2.5725"/>```
```</inertial>```

The variables ```mass```, ```origin``` and ```inertia``` are typical of SDF and URDF files. The variable ```xacro:property``` instead are only used by the xacro interpreter.

**NOTE: if statements in xacro**
To write conditional statements use the following syntax:
```<xacro:if value="${data['mesh']}">```
```     Do something```
```</xacro:if>```
This reads as: if ```mesh``` is true then ```Do something```.
To include an else use:
```<xacro:unless value="${data['mesh']}">```
```     Do something else```
```</xacro:unless>```

**NOTE: parameterize the yaml selection**
Depending whether the has_differential flag is on, select the correct yaml file.
```<xacro:if value="${has_differential}">```
```     <xacro:property name="filename" value="$(find robot4ws_description)/urdf/config/body_only.yaml"/>```
```</xacro:if>```
```<xacro:unless value="${has_differential}">```
```     <xacro:property name="filename" value="$(find robot4ws_description)/urdf/config/body.yaml"/>```
```</xacro:unless>```

#### Joints definition
We need to define mainly ```parent```, ```child```, ```origin``` and ```axis```. Others are available, e.g. ```limit```, ```dynamics```, etc. This way you can setup springs, dampers, etc.
With ```parent```, we consider the previous link.
With ```child```, we consider the current link, on which the link body is attached.
The ```origin``` describes the location (x, y, z, r, p, y) of the joint with respect to the previous joint.
The ```axis``` describes the orientation (x, y, z) of the joint axis.

Then we have to define the joint itself
```
joint:
    type: "continuous"
    origin:
        position:
            x: 0
            y: 0
            z: 0

        orientation:
            roll: 0
            pitch: 0
            yaw: 0
```

## Dependencies
* to-do