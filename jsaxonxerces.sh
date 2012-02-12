# Saxon with Xerces parser. $1 is myfile.html :: $2 is myfile.xml
DOCBOOK_HTML_XSL_FILE=/usr/share/sgml/docbook/xsl-stylesheets-1.73.2/html/docbook.xsl
java -Djavax.xml.parsers.DocumentBuilderFactory=org.apache.xerces.jaxp.DocumentBuilderFactoryImpl \
     -Djavax.xml.parsers.SAXParserFactory=org.apache.xerces.jaxp.SAXParserFactoryImpl \
     com.icl.saxon.StyleSheet -o "$1" "$2" $DOCBOOK_HTML_XSL_FILE
