<map version="freeplane 1.9.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="PyQt" FOLDED="false" ID="ID_696401721" CREATED="1610381621824" MODIFIED="1649442766776" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_icon_for_attributes="true" show_note_icons="true" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="DEFAULT" ENDARROW="NONE"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent CONTENT-TYPE="plain/auto" TYPE="DETAILS"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#4e85f8" STYLE="bubble" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#4e85f8"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="3" RULE="ON_BRANCH_CREATION"/>
<node TEXT="pythospot course" POSITION="right" ID="ID_229700571" CREATED="1649442702828" MODIFIED="1649442775268" LINK="https://pythonspot.com/pyqt5-window/">
<edge COLOR="#ff0000"/>
<node TEXT="QtWidget" ID="ID_1273326380" CREATED="1649442736971" MODIFIED="1649442761015"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; color: rgb(0, 0, 0); font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; word-spacing: 0px"><font color="rgb(133, 153, 0)">import</font> sys<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtWidgets <font color="rgb(133, 153, 0)">import</font> QApplication, QWidget<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtGui <font color="rgb(133, 153, 0)">import</font> QIcon<br/><br/><font color="rgb(133, 153, 0)">class</font> <font color="rgb(181, 137, 0)">App</font>(QWidget):<br/><br/>    <font color="rgb(133, 153, 0)">def</font> __init__(self):<br/>        super().__init__()<br/>        self.title = <font color="rgb(42, 161, 152)">'PyQt5 simple window - pythonspot.com'</font><br/>        self.left = <font color="rgb(42, 161, 152)">10</font><br/>        self.top = <font color="rgb(42, 161, 152)">10</font><br/>        self.width = <font color="rgb(42, 161, 152)">640</font><br/>        self.height = <font color="rgb(42, 161, 152)">480</font><br/>        self.initUI()<br/>        <br/>    <font color="rgb(133, 153, 0)">def</font> initUI(self):<br/>        self.setWindowTitle(self.title)<br/>        self.setGeometry(self.left, self.top, self.width, self.height)<br/>        self.show()<br/>    <br/><font color="rgb(133, 153, 0)">if</font> __name__ == <font color="rgb(42, 161, 152)">'__main__'</font>:<br/>    app = QApplication(sys.argv)<br/>    ex = App()<br/>    sys.exit(app.exec_())<br/></pre>
  </body>
</html></richcontent>
</node>
<node TEXT="QtMainWindow" ID="ID_1518106502" CREATED="1649442707028" MODIFIED="1649442738129"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; color: rgb(0, 0, 0); font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; word-spacing: 0px"><font color="rgb(133, 153, 0)">import</font> sys<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtWidgets <font color="rgb(133, 153, 0)">import</font> QApplication, QWidget, QMainWindow<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtGui <font color="rgb(133, 153, 0)">import</font> QIcon<br/><br/><font color="rgb(133, 153, 0)">class</font> <font color="rgb(181, 137, 0)">App</font>(QMainWindow):<br/><br/>    <font color="rgb(133, 153, 0)">def</font> __init__(self):<br/>        super().__init__()<br/>        self.title = <font color="rgb(42, 161, 152)">'PyQt5 status bar example - pythonspot.com'</font><br/>        self.left = <font color="rgb(42, 161, 152)">10</font><br/>        self.top = <font color="rgb(42, 161, 152)">10</font><br/>        self.width = <font color="rgb(42, 161, 152)">640</font><br/>        self.height = <font color="rgb(42, 161, 152)">480</font><br/>        self.initUI()<br/><br/>    <font color="rgb(133, 153, 0)">def</font> initUI(self):<br/>        self.setWindowTitle(self.title)<br/>        self.setGeometry(self.left, self.top, self.width, self.height)<br/>        self.statusBar().showMessage(<font color="rgb(42, 161, 152)">'Message in statusbar.'</font>)<br/>        self.show()<br/><br/><font color="rgb(133, 153, 0)">if</font> __name__ == <font color="rgb(42, 161, 152)">'__main__'</font>:<br/>    app = QApplication(sys.argv)<br/>    ex = App()<br/>    sys.exit(app.exec_())</pre>
  </body>
</html></richcontent>
</node>
<node TEXT="PyQt5 signals and slots" ID="ID_937725614" CREATED="1649443534949" MODIFIED="1649443564073"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p style="line-height: 25px; color: rgb(0, 0, 0); font-family: arial, sans-serif; font-size: 17px; font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px">
      Graphical applications (GUI) are event-driven, unlike console or terminal applications. A users action like clicks a button or selecting an item in a list is called an event.
    </p>
    <p style="line-height: 25px; color: rgb(0, 0, 0); font-family: arial, sans-serif; font-size: 17px; font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px">
      <b>If an event takes place, each PyQt5 widget can emit a signal</b>. A signal does not execute any action, that is done by a <b>slot</b>.
    </p>
  </body>
</html></richcontent>
<node TEXT="example" ID="ID_881302815" CREATED="1649443576084" MODIFIED="1649444694410"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; color: rgb(0, 0, 0); font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; word-spacing: 0px">button.clicked.connect(self.slot_method)</pre>
    <p>
      <font color="rgb(0, 0, 0)" face="arial, sans-serif">The button click (signal) is connected to the action (slot). In this example, the method slot_method will be called if the signal emits.</font>
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="for all widgets" ID="ID_1814908306" CREATED="1649443625268" MODIFIED="1649443908900"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p style="line-height: 25px; color: rgb(0, 0, 0); font-family: arial, sans-serif; font-size: 17px; font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px">
      This principle of connecting slots methods or function to a widget, applies to all widgets,
    </p>
    <font color="rgb(0, 0, 0)" face="arial, sans-serif"><figure class="highlight python" align="start" style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-left: 0px; padding-right: 0px; letter-spacing: normal; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px"/>
    </font>

    <table style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
      <tr style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
        <td class="code" style="border-top-style: none; border-top-width: 0px; border-right-style: none; border-right-width: 0px; border-bottom-style: none; border-bottom-width: 0px; border-left-style: none; border-left-width: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
          <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px"><br/>


widget.signal.connect(slot_method)<br/><br/></pre>
        </td>
      </tr>
    </table>
<figure/>    

    <p style="line-height: 25px; color: rgb(0, 0, 0); font-family: arial, sans-serif; font-size: 17px; font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px">
      or we can explicitly define the signal:
    </p>
    <font color="rgb(0, 0, 0)" face="arial, sans-serif"><figure class="highlight python" align="start" style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-left: 0px; padding-right: 0px; letter-spacing: normal; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px"/>
    </font>

    <table style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
      <tr style="margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
        <td class="code" style="border-top-style: none; border-top-width: 0px; border-right-style: none; border-right-width: 0px; border-bottom-style: none; border-bottom-width: 0px; border-left-style: none; border-left-width: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; width: 720px">
          <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px"><br/>


QtCore.QObject.connect(widget, QtCore.SIGNAL(‘signalname’), slot_function)<br/><br/></pre>
        </td>
      </tr>
    </table>
<figure/>    

    <p style="line-height: 25px; color: rgb(0, 0, 0); font-family: arial, sans-serif; font-size: 17px; font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; white-space: normal; word-spacing: 0px">
      PyQt supports many type of signals, not just clicks.
    </p>
  </body>
</html></richcontent>
</node>
<node TEXT="Full example" ID="ID_1963113099" CREATED="1649443908875" MODIFIED="1649443916538"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; color: rgb(0, 0, 0); font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; word-spacing: 0px"><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">from</font></span><span class="line" style="height: 20px"> PyQt5.QtWidgets </span><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">import</font></span><span class="line" style="height: 20px"> (QApplication, QComboBox, QDialog,</span><br/><span class="line" style="height: 20px">QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,</span><br/><span class="line" style="height: 20px">QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,</span><br/><span class="line" style="height: 20px">QVBoxLayout)</span><br/><br/><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">import</font></span><span class="line" style="height: 20px"> sys</span><br/><br/><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">class</font></span><span class="class"> </span><span class="title" style="color: rgb(181, 137, 0)"><font color="rgb(181, 137, 0)">Dialog</font></span><span class="class">(</span><span class="params">QDialog</span><span class="class">):</span><br/><br/><span class="line" style="height: 20px">    </span><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">def</font></span><span class="function"> </span><span class="title">slot_method</span><span class="function">(</span><span class="params">self</span><span class="function">):</span><br/><span class="line" style="height: 20px">        </span><span class="built_in">print</span><span class="line" style="height: 20px">(</span><span class="string" style="color: rgb(42, 161, 152)"><font color="rgb(42, 161, 152)">'slot method called.'</font></span><span class="line" style="height: 20px">)</span><br/><span class="line" style="height: 20px">    </span><br/><span class="line" style="height: 20px">    </span><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">def</font></span><span class="function"> </span><span class="title">__init__</span><span class="function">(</span><span class="params">self</span><span class="function">):</span><br/><span class="line" style="height: 20px">        </span><span class="built_in">super</span><span class="line" style="height: 20px">(Dialog, self).__init__()</span><br/><span class="line" style="height: 20px">        </span><br/><span class="line" style="height: 20px">        button=QPushButton(</span><span class="string" style="color: rgb(42, 161, 152)"><font color="rgb(42, 161, 152)">&quot;Click&quot;</font></span><span class="line" style="height: 20px">)</span><br/><span class="line" style="height: 20px">        button.clicked.connect(self.slot_method)</span><br/><span class="line" style="height: 20px">        </span><br/><span class="line" style="height: 20px">        mainLayout = QVBoxLayout()</span><br/><span class="line" style="height: 20px">        mainLayout.addWidget(button)</span><br/><span class="line" style="height: 20px">        </span><br/><span class="line" style="height: 20px">        self.setLayout(mainLayout)</span><br/><span class="line" style="height: 20px">        self.setWindowTitle(</span><span class="string" style="color: rgb(42, 161, 152)"><font color="rgb(42, 161, 152)">&quot;Button Example - pythonspot.com&quot;</font></span><span class="line" style="height: 20px">)</span><br/><br/><span class="keyword" style="color: rgb(133, 153, 0)"><font color="rgb(133, 153, 0)">if</font></span><span class="line" style="height: 20px"> __name__ == </span><span class="string" style="color: rgb(42, 161, 152)"><font color="rgb(42, 161, 152)">'__main__'</font></span><span class="line" style="height: 20px">:</span><br/><span class="line" style="height: 20px">    app = QApplication(sys.argv)</span><br/><span class="line" style="height: 20px">    dialog = Dialog()</span><br/><span class="line" style="height: 20px">    sys.exit(dialog.exec_())</span></pre>
  </body>
</html></richcontent>
</node>
</node>
<node TEXT="messagebox" ID="ID_517495689" CREATED="1649443714610" MODIFIED="1649443750684">
<node TEXT="Example" ID="ID_767077355" CREATED="1649443961259" MODIFIED="1649444038097"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <pre style="padding-top: 5px; padding-bottom: 5px; padding-right: 10px; padding-left: 10px; font-size: 13px; font-family: monospace !important; background-color: rgb(242, 242, 242); background-image: null; background-repeat: repeat; background-attachment: scroll; background-position: null; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; color: rgb(0, 0, 0); font-style: normal; font-weight: 400; letter-spacing: normal; text-align: start; text-indent: 0px; text-transform: none; word-spacing: 0px"><br/>


<font color="rgb(133, 153, 0)">import</font> sys<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtWidgets <font color="rgb(133, 153, 0)">import</font> QApplication, QWidget, QPushButton, QMessageBox<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtGui <font color="rgb(133, 153, 0)">import</font> QIcon<br/><font color="rgb(133, 153, 0)">from</font> PyQt5.QtCore <font color="rgb(133, 153, 0)">import</font> pyqtSlot<br/><br/><font color="rgb(133, 153, 0)">class</font> <font color="rgb(181, 137, 0)">App</font>(QWidget):<br/><br/>    <font color="rgb(133, 153, 0)">def</font> __init__(self):<br/>        super().__init__()<br/>        self.title = <font color="rgb(42, 161, 152)">'PyQt5 messagebox - pythonspot.com'</font><br/>        self.left = <font color="rgb(42, 161, 152)">10</font><br/>        self.top = <font color="rgb(42, 161, 152)">10</font><br/>        self.width = <font color="rgb(42, 161, 152)">320</font><br/>        self.height = <font color="rgb(42, 161, 152)">200</font><br/>        self.initUI()<br/>        <br/>    <font color="rgb(133, 153, 0)">def</font> initUI(self):<br/>        self.setWindowTitle(self.title)<br/>        self.setGeometry(self.left, self.top, self.width, self.height)<br/><br/><b>        buttonReply = QMessageBox.question(self, <font color="rgb(42, 161, 152)">'PyQt5 message'</font>, <font color="rgb(42, 161, 152)">&quot;Do you like PyQt5?&quot;</font>, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)<br/>        <font color="rgb(133, 153, 0)">if</font> buttonReply == QMessageBox.Yes:<br/>            print(<font color="rgb(42, 161, 152)">'Yes clicked.'</font>)<br/>        <font color="rgb(133, 153, 0)">else</font>:<br/>            print(<font color="rgb(42, 161, 152)">'No clicked.'</font>)<br/></b><br/>        self.show()<br/>        <br/><font color="rgb(133, 153, 0)">if</font> __name__ == <font color="rgb(42, 161, 152)">'__main__'</font>:<br/>    app = QApplication(sys.argv)<br/>    ex = App()<br/>    sys.exit(app.exec_())  </pre>
  </body>
</html></richcontent>
</node>
<node TEXT="available buttons" FOLDED="true" ID="ID_1222679758" CREATED="1649444038073" MODIFIED="1649444428359">
<icon BUILTIN="bookmark"/>
<node TEXT="QMessageBox.Cancel" ID="ID_604338377" CREATED="1649444281918" MODIFIED="1649444336736"/>
<node TEXT="QMessageBox.Ok" ID="ID_1280449603" CREATED="1649444337390" MODIFIED="1649444344031"/>
<node TEXT="QMessageBox.Help" ID="ID_285082326" CREATED="1649444340686" MODIFIED="1649444341952"/>
<node TEXT="QMessageBox.Open" ID="ID_19449332" CREATED="1649444281918" MODIFIED="1649444349167"/>
<node TEXT="QMessageBox.Save" ID="ID_866658975" CREATED="1649444350077" MODIFIED="1649444351678"/>
<node TEXT="QMessageBox.SaveAll" ID="ID_175990344" CREATED="1649444352350" MODIFIED="1649444353183"/>
<node TEXT="QMessageBox.Discard" ID="ID_1977796420" CREATED="1649444281923" MODIFIED="1649444360167"/>
<node TEXT="QMessageBox.Close" ID="ID_1863183708" CREATED="1649444416613" MODIFIED="1649444417935"/>
<node TEXT="QMessageBox.Apply" ID="ID_1555843991" CREATED="1649444418453" MODIFIED="1649444421490"/>
<node TEXT="QMessageBox.Reset" ID="ID_1656361533" CREATED="1649444281927" MODIFIED="1649444428358"/>
<node TEXT="QMessageBox.Yes" ID="ID_1528554277" CREATED="1649444379053" MODIFIED="1649444380823"/>
<node TEXT="QMessageBox.YesToAll" ID="ID_129839618" CREATED="1649444381173" MODIFIED="1649444382047"/>
<node TEXT="QMessageBox.No" ID="ID_1317769578" CREATED="1649444281930" MODIFIED="1649444384736"/>
<node TEXT="QMessageBox.NoToAll" ID="ID_1656644419" CREATED="1649444385262" MODIFIED="1649444386624"/>
<node ID="ID_691098325" CREATED="1649444386934" MODIFIED="1649444386934"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      QMessageBox.NoButton
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="QMessageBox.RestoreDefaults" ID="ID_1078334818" CREATED="1649444281932" MODIFIED="1649444391863"/>
<node TEXT="QMessageBox.Abort" ID="ID_812479289" CREATED="1649444392222" MODIFIED="1649444400222"/>
<node ID="ID_323496886" CREATED="1649444400534" MODIFIED="1649444400534"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      QMessageBox.Retry
    </p>
  </body>
</html>
</richcontent>
</node>
<node ID="ID_1360206481" CREATED="1649444281935" MODIFIED="1649444281935"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      QMessageBox.Ignore
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
</node>
<node TEXT="QLineEdit" ID="ID_1872930636" CREATED="1649444462772" MODIFIED="1649444473670">
<node TEXT="example" ID="ID_480573934" CREATED="1649444477101" MODIFIED="1649444523541"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      self.textbox = QLineEdit(self)
    </p>
    <p>
      self.textbox.move(20, 20)
    </p>
    <p>
      self.textbox.resize(280,40)
    </p>
  </body>
</html></richcontent>
<node TEXT="textboxValue = self.textbox.text()" ID="ID_1752601362" CREATED="1649444533334" MODIFIED="1649444533877"/>
</node>
<node TEXT="methods" ID="ID_1588550997" CREATED="1649444616332" MODIFIED="1649444618271">
<node TEXT="setText()" ID="ID_1382950057" CREATED="1649444611892" MODIFIED="1649444614885"/>
</node>
<node TEXT="attributes" ID="ID_883295323" CREATED="1649444623932" MODIFIED="1649444628869">
<node TEXT="text()" ID="ID_1735826979" CREATED="1649444634090" MODIFIED="1649444634090"/>
</node>
</node>
<node TEXT="absolute position" ID="ID_398023471" CREATED="1649444661366" MODIFIED="1649444661366">
<node TEXT="move method" ID="ID_642751865" CREATED="1649444726172" MODIFIED="1649444728756"/>
</node>
<node TEXT="menu" ID="ID_1343051128" CREATED="1649444723163" MODIFIED="1649444764890"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      To create a menu for a PyQt5 program we need to use a QMainWindow.
    </p>
    <p>
      This type of menu is visible in many applications and shows right below the window bar. It usually has a file and edit sub menu.
    </p>
  </body>
</html>
</richcontent>
<node TEXT="example" ID="ID_1788711774" CREATED="1649444748741" MODIFIED="1649444795605"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      
    </p>
    <p>
      mainMenu = self.menuBar()
    </p>
    <p>
      fileMenu = mainMenu.addMenu('File')
    </p>
    <p>
      editMenu = mainMenu.addMenu('Edit')
    </p>
    <p>
      viewMenu = mainMenu.addMenu('View')
    </p>
    <p>
      searchMenu = mainMenu.addMenu('Search')
    </p>
    <p>
      toolsMenu = mainMenu.addMenu('Tools')
    </p>
    <p>
      helpMenu = mainMenu.addMenu('Help')
    </p>
    <p>
      
    </p>
    <p>
      <i>ndividual buttons can be added to the menus like this:</i>
    </p>
    <p>
      
    </p>
    <p>
      
    </p>
    <p>
      exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
    </p>
    <p>
      exitButton.setShortcut('Ctrl+Q')
    </p>
    <p>
      exitButton.setStatusTip('Exit application')
    </p>
    <p>
      exitButton.triggered.connect(self.close)
    </p>
    <p>
      fileMenu.addAction(exitButton)
    </p>
  </body>
</html>
</richcontent>
<node TEXT="full code" ID="ID_92705613" CREATED="1649444796747" MODIFIED="1649444804951"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      
    </p>
    <p>
      import sys
    </p>
    <p>
      from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction
    </p>
    <p>
      from PyQt5.QtGui import QIcon
    </p>
    <p>
      from PyQt5.QtCore import pyqtSlot
    </p>
    <p>
      
    </p>
    <p>
      class App(QMainWindow):
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;def __init__(self):
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;super().__init__()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.title = 'PyQt5 menu - pythonspot.com'
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.left = 10
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.top = 10
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.width = 640
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.height = 400
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.initUI()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;def initUI(self):
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.setWindowTitle(self.title)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.setGeometry(self.left, self.top, self.width, self.height)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mainMenu = self.menuBar()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fileMenu = mainMenu.addMenu('File')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;editMenu = mainMenu.addMenu('Edit')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;viewMenu = mainMenu.addMenu('View')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;searchMenu = mainMenu.addMenu('Search')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;toolsMenu = mainMenu.addMenu('Tools')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;helpMenu = mainMenu.addMenu('Help')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exitButton.setShortcut('Ctrl+Q')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exitButton.setStatusTip('Exit application')
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;exitButton.triggered.connect(self.close)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;fileMenu.addAction(exitButton)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.show()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;
    </p>
    <p>
      if __name__ == '__main__':
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;app = QApplication(sys.argv)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;ex = App()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;sys.exit(app.exec_())
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
</node>
</node>
<node TEXT="Classes" POSITION="right" ID="ID_688942099" CREATED="1649442851651" MODIFIED="1649442853988">
<edge COLOR="#0000ff"/>
<node TEXT="Windows and dialogs" ID="ID_1887312009" CREATED="1649442890594" MODIFIED="1649442901292">
<node TEXT="QtWidget" ID="ID_712382659" CREATED="1649442857708" MODIFIED="1649442861132"/>
<node TEXT="QtMainWindow" ID="ID_1452349607" CREATED="1649442861274" MODIFIED="1649442865341">
<node TEXT="Already has a layout" ID="ID_1057684242" CREATED="1649443887923" MODIFIED="1649443893771"/>
<node TEXT="can accommodate a menu" ID="ID_767558335" CREATED="1649444739274" MODIFIED="1649444745044"/>
</node>
<node TEXT="QInputDialog," ID="ID_15495474" CREATED="1649442876690" MODIFIED="1649442884891"/>
<node TEXT="QLineEdit," ID="ID_617366207" CREATED="1649442885490" MODIFIED="1649442887500"/>
<node ID="ID_532056321" CREATED="1649442887761" MODIFIED="1649442887761"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      QFileDialog
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="Widgets" ID="ID_1359213916" CREATED="1649444450885" MODIFIED="1649444455167">
<node TEXT="methods" ID="ID_1329534846" CREATED="1649444674386" MODIFIED="1649444678596">
<node TEXT="move(x,y)" ID="ID_851382583" CREATED="1649444679332" MODIFIED="1649444685998"/>
<node TEXT="connect" ID="ID_1233566409" CREATED="1649444688475" MODIFIED="1649444693856"/>
</node>
<node TEXT="Slider" ID="ID_1291787882" CREATED="1649444943313" MODIFIED="1649445066529">
<node TEXT="example" ID="ID_211075635" CREATED="1649445068328" MODIFIED="1649445099525" LINK="https://pythonbasics.org/qslider/"><richcontent TYPE="NOTE" CONTENT-TYPE="xml/">
<html>
  <head>
    
  </head>
  <body>
    <p>
      import sys
    </p>
    <p>
      from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider
    </p>
    <p>
      from PyQt5.QtCore import Qt
    </p>
    <p>
      
    </p>
    <p>
      class Example(QMainWindow):
    </p>
    <p>
      
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;def __init__(self):
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;super().__init__()
    </p>
    <p>
      
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mySlider = QSlider(Qt.Horizontal, self)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mySlider.setGeometry(30, 40, 200, 30)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mySlider.valueChanged[int].connect(self.changeValue)
    </p>
    <p>
      
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.setGeometry(50,50,320,200)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.setWindowTitle(&quot;Checkbox Example&quot;)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.show()
    </p>
    <p>
      
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;def changeValue(self, value):
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print(value)
    </p>
    <p>
      
    </p>
    <p>
      if __name__ == '__main__':
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;app = QApplication(sys.argv)
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;ex = Example()
    </p>
    <p>
      &nbsp;&nbsp;&nbsp;&nbsp;sys.exit(app.exec_())
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
</node>
<node TEXT="Layouts" ID="ID_1676566076" CREATED="1649443751714" MODIFIED="1649443755500">
<node TEXT="QVBoxLayout" ID="ID_1448326788" CREATED="1649443770675" MODIFIED="1649443771067"/>
</node>
<node TEXT="menu" ID="ID_323577969" CREATED="1649444720084" MODIFIED="1649444722358"/>
</node>
<node TEXT="links" POSITION="left" ID="ID_1072921783" CREATED="1649445081495" MODIFIED="1649445082793">
<edge COLOR="#00ff00"/>
<node TEXT="https://pythonbasics.org/qslider/" ID="ID_912972242" CREATED="1649445083760" MODIFIED="1649445084896"/>
</node>
</node>
</map>
