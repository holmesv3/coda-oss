/*
 * =========================================================================
 * This file is part of xml.lite-python (nanobind bindings)
 * =========================================================================
 *
 * (C) Copyright 2004 - 2024, MDA Information Systems LLC
 *
 * xml.lite-python is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; If not,
 * see <http://www.gnu.org/licenses/>.
 */

#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include "import/xml/lite.h"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(coda_xml_lite, m) {
    m.doc() = "CODA-OSS XML lite parsing";
    
    // Element class
    nb::class_<xml::lite::Element>(m, "Element")
        .def(nb::init<>())
        .def(nb::init<const std::string&>(), "qname"_a)
        .def(nb::init<const std::string&, const std::string&>(), 
             "qname"_a, "uri"_a)
        .def(nb::init<const std::string&, const std::string&, const std::string&>(),
             "qname"_a, "uri"_a, "characterData"_a)
        // Character data methods
        .def("setCharacterData", 
             static_cast<void (xml::lite::Element::*)(const std::string&)>(&xml::lite::Element::setCharacterData), 
             "data"_a)
        .def("getCharacterData", 
             static_cast<std::string (xml::lite::Element::*)() const>(&xml::lite::Element::getCharacterData))
        // QName methods
        .def("getLocalName", &xml::lite::Element::getLocalName)
        .def("getUri", 
             static_cast<std::string (xml::lite::Element::*)() const>(&xml::lite::Element::getUri))
        .def("setQName", 
             static_cast<void (xml::lite::Element::*)(const std::string&)>(&xml::lite::Element::setQName),
             "qname"_a)
        // Attributes - expose only the const getter to avoid setAttributes/getAttributes issues
        .def("getAttributes", 
             nb::overload_cast<>(&xml::lite::Element::getAttributes, nb::const_),
             nb::rv_policy::reference_internal)
        .def("attribute", 
             [](xml::lite::Element& self, const std::string& key) -> std::string& {
                 return self.attribute(key);
             },
             "key"_a,
             nb::rv_policy::reference_internal)
        // Element query methods
        .def("getElementsByTagName", 
             [](const xml::lite::Element& self, const std::string& localName, bool recurse) {
                 return self.getElementsByTagName(localName, recurse);
             },
             "localName"_a, "recurse"_a = false)
        .def("getElementsByTagNameNS",
             [](const xml::lite::Element& self, const std::string& qname, bool recurse) {
                 return self.getElementsByTagNameNS(qname, recurse);
             },
             "qname"_a, "recurse"_a = false)
        // Children methods
        .def("getChildren", 
             nb::overload_cast<>(&xml::lite::Element::getChildren, nb::const_),
             nb::rv_policy::reference_internal)
        .def("getChild", 
             [](const xml::lite::Element& self, const std::string& localName) -> xml::lite::Element* {
                 std::vector<xml::lite::Element*> children = self.getChildren();
                 for (auto* child : children) {
                     if (child && child->getLocalName() == localName) {
                         return child;
                     }
                 }
                 return nullptr;
             },
             "localName"_a,
             nb::rv_policy::reference_internal)
        // Note: addChild, setChild methods that take raw pointers are ignored
        // to avoid memory management issues. Use Document to build trees.
        .def("destroyChildren", &xml::lite::Element::destroyChildren)
        .def("clone", &xml::lite::Element::clone, "element"_a)
        // Print methods
        .def("prettyPrint", 
             [](const xml::lite::Element& self) {
                 io::StringStream ss;
                 self.prettyPrint(ss);
                 return ss.stream().str();
             })
        .def("print", 
             [](const xml::lite::Element& self) {
                 io::StringStream ss;
                 self.print(ss);
                 return ss.stream().str();
             });
    
    // Attributes class
    nb::class_<xml::lite::Attributes>(m, "Attributes")
        .def(nb::init<>())
        .def("getLength", &xml::lite::Attributes::getLength)
        .def("getIndex", 
             nb::overload_cast<const std::string&>(&xml::lite::Attributes::getIndex, nb::const_),
             "qname"_a)
        .def("getValue", 
             static_cast<std::string (xml::lite::Attributes::*)(int) const>(&xml::lite::Attributes::getValue),
             "i"_a)
        .def("getQName", 
             static_cast<std::string (xml::lite::Attributes::*)(int) const>(&xml::lite::Attributes::getQName),
             "i"_a)
        .def("getUri", 
             static_cast<std::string (xml::lite::Attributes::*)(int) const>(&xml::lite::Attributes::getUri),
             "i"_a)
        .def("add", 
             [](xml::lite::Attributes& self, const std::string& qname, const std::string& value) {
                 xml::lite::AttributeNode node;
                 node.setQName(qname);
                 node.setValue(value);
                 self.add(node);
             },
             "qname"_a, "value"_a);
    
    // Document class
    nb::class_<xml::lite::Document>(m, "Document")
        .def(nb::init<>())
        .def(nb::init<xml::lite::Element*, bool>(), 
             "rootNode"_a, "own"_a = true)
        .def("getRootElement", 
             static_cast<xml::lite::Element* (xml::lite::Document::*)(bool)>(&xml::lite::Document::getRootElement),
             "steal"_a = false,
             nb::rv_policy::reference_internal)
        .def("setRootElement", 
             [](xml::lite::Document& self, xml::lite::Element* root, bool own) {
                 self.setRootElement(root, own);
             },
             "root"_a, "own"_a = true)
        .def("destroy", &xml::lite::Document::destroy);
    
    // MinidomParser class
    nb::class_<xml::lite::MinidomParser>(m, "MinidomParser")
        .def(nb::init<bool>(), "storeEncoding"_a = true)
        .def("parse", 
             [](xml::lite::MinidomParser& self, const std::string& xmlContent) {
                 io::StringStream ss;
                 ss.write(xmlContent);
                 self.parse(ss, xmlContent.size());
             },
             "xmlContent"_a)
        .def("parseFile",
             [](xml::lite::MinidomParser& self, const std::string& filename) {
                 io::FileInputStream fis(filename);
                 self.parse(fis);
             },
             "filename"_a)
        .def("getDocument", 
             [](xml::lite::MinidomParser& self) -> xml::lite::Document* {
                 return self.getDocument();
             },
             nb::rv_policy::reference_internal)
        .def("clear", &xml::lite::MinidomParser::clear);
    
    // XMLReader class (if needed - basic wrapper)
    nb::class_<xml::lite::XMLReader>(m, "XMLReader")
        .def(nb::init<>());
    
    // MinidomHandler class (if needed - basic wrapper)
    nb::class_<xml::lite::MinidomHandler>(m, "MinidomHandler")
        .def(nb::init<>());
}
