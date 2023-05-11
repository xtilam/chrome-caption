import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Layouts 1.12
ApplicationWindow{
    id: win
    width: 400
    height: 500
    visible: true
    title: "Chrome"
    x: 0
    y: 0
    font.pixelSize: 14
    property string error: "";
    property bool isValidAddress: true;
    property string memoryText: "";
    property bool isStartPress: false;

    ColumnLayout{
        width: parent.width - 10
        spacing: 2
        anchors{
            margins: 5
            top: parent.top
            left: parent.left
        }
        visible: !isValidAddress
        Button{
            Layout.fillWidth: true
            text: "Check Chrome"
            id: checkChrome
            onClicked: function(){
                checkChrome.enabled = false;
                let isSucces = actions.checkChrome()
                checkChrome.enabled = true;
            }
        }
        Text{
            text: error
            color: "red"
            visible: error ? true : false
        }
    }
    
    ColumnLayout{
        width: parent.width - 10
        height: parent.height - 10
        spacing: 2
        anchors{
            margins: 5
            top: parent.top
            left: parent.left
        }
        visible: isValidAddress
        RowLayout {
            Layout.fillWidth: true
            Button{
                 Layout.fillWidth: true
                 text: "Show Caption"
                 onClicked: function(){
                     actions.showCaption()
                 }
            }
            Button{
                 Layout.fillWidth: true
                 text: "Hide Caption"
                 onClicked: function(){
                     actions.hideCaption()
                 }
            }
        }
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            TextArea {
                id: text
                width: parent.width
                text: memoryText
                selectByMouse: true
                wrapMode: TextEdit.Wrap
                cursorPosition: memoryText.length
            }
        }
    }
    
    Timer{
        running: isValidAddress
        interval: 500
        repeat: true
        onTriggered: function(){
            if(text.selectedText) return
            actions.getText()
        }
    }
    Component.onCompleted: {
        actions.setViewWin(win)
    }
}
