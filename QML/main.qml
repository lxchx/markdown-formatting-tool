import QtQuick 2.14
import QtQuick.Window 2.2
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Window {
    id: root
    visible: true
    width: 350; height: 200

    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
    color: "#801e80e9"

    Component.onCompleted: {
        function initEffect(){
            tool.set_no_focus(root)
            tool.setAeroEffect(root)
        }

        tool.load_model()

        Qt.callLater(initEffect)
    }

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton

        onPositionChanged: {
            tool.move_window(root)
        }
    }

    ColumnLayout {
        id: columnLayout
        spacing: 0
        anchors.fill: parent

        Rectangle {
            id: rectangle
            color: "#6e4c5359"
            Layout.maximumHeight: 20
            Layout.preferredHeight: 20
            Layout.fillWidth: true

            RowLayout {
                id: rowLayout
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right

                Rectangle {
                    width: 50
                    Layout.fillHeight: true
                    color: editMouseArea.hovered ? "#6e4c5359" : "#00000000"

                    Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.OutQuad
                        duration: 200
                    }
                }

                    MouseArea {
                        id: editMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        property bool hovered: false

                        onEntered: hovered = true
                        onExited: hovered = false

                        onPressed: tool.edit()
                    }

                    Label {
                        anchors.fill: parent

                        text: qsTr("编辑")
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.family: "Microsoft YaHei"
                        font.pointSize: 10
                    }
                }

                Rectangle {
                    width: 50
                    Layout.fillHeight: true
                    color: exitMouseArea.hovered ? "#6e4c5359" : "#00000000"

                    Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.OutQuad
                        duration: 200
                    }
                }

                    MouseArea {
                        id: exitMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        property bool hovered: false

                        onEntered: hovered = true
                        onExited: hovered = false

                        onPressed: Qt.quit()
                    }

                    Label {
                        anchors.fill: parent

                        text: qsTr("退出")
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.family: "Microsoft YaHei"
                        font.pointSize: 10
                    }
                }
            }
        }

        GridView {
            id: grid
            Layout.fillHeight: true
            Layout.fillWidth: true
            boundsMovement: Flickable.StopAtBounds
            interactive: false

            clip: true

            cellWidth: width/4
            cellHeight: height/Math.ceil(count/4.0)

            model: tool.model
            delegate: Rectangle {
                id: rect
                width: grid.cellWidth
                height: grid.cellHeight
                color: mouseArea.hovered ? "#6e4c5359" : "#00000000"

                Behavior on color {
                    ColorAnimation {
                        easing.type: Easing.OutQuad
                        duration: 200
                    }
                }

                Label {
                    id: label
                    text: display_text
                    font.family: "Microsoft YaHei"
                    font.pointSize: 13
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    anchors.fill: parent

                    ToolTip {
                        id: toolTip
                        parent: label
                        delay: 500
                        timeout: 3000
                        visible: mouseArea.hovered
                        text: description
                    }
                }

                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    acceptedButtons: Qt.LeftButton

                    property bool is_move: false

                    property int last_x: 0  //记录一下前后的x轴变化，用来粗糙地检测有没有窗口移动

                    Component.onCompleted: last_x = mouseArea.mapToGlobal(0,0).x

                    onPositionChanged: {
                        tool.move_window(root)
                    }

                    onPressed: last_x = mouseArea.mapToGlobal(0,0).x

                    onReleased: {
                        //console.log(last_x)
                        //console.log(mouseArea.mapToGlobal(0,0).x)
                        if(Math.abs(mouseArea.mapToGlobal(0,0).x - last_x) < 1){
                            console.log(operation)
                            tool.oparate(operation)
                        }
                    }
                    

                    property bool hovered: false

                    onEntered: hovered = true
                    onExited: hovered = false
                }
            }
        }

    }
}


