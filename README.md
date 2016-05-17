Some commands to run in the shell. Probably can be and should be put into a grunt / gulp / etc build tool script, but here goes:

npm install -g browserify watchify
npm install reactify
npm install react react-dom

watchify -t reactify components/Chat.js -o bundle.js -v
