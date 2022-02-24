const chatButton = document.querySelector('.chatbox_button');
const chatContent = document.querySelector('.chatbox_support');
const icons = {
    isClicked: '<img src="../static/images/chatbox-icon.svg" />',
    isNotClicked: '<img src="../static/images/chatbox-icon.svg" />'
}
const chatbox = new InteractiveChatbox(chatButton, chatContent, icons);
chatbox.display();
chatbox.toggleIcon(false, chatButton);