#!/usr/bin/env python3
#
# Tests the importer for SBML.
#
# This file is part of Myokit.
# See http://myokit.org for copyright, sharing, and licensing details.
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals

import os
import unittest

import myokit
import myokit.formats as formats

from shared import DIR_FORMATS

# Unit testing in Python 2 and 3
try:
    unittest.TestCase.assertRaisesRegex
except AttributeError:  # pragma: no python 3 cover
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

# Strings in Python 2 and 3
try:
    basestring
except NameError:   # pragma: no python 2 cover
    basestring = str


class SBMLTest(unittest.TestCase):
    """
    Tests the SBML importer. First correct construction of myokit model
    is tested using an altered model from the SBML test suite. Then
    handling of errors or misspecified files is checked.
    """
    @classmethod
    def setUpClass(cls):
        """
        Tests case 00004 from the SBML test suite
        http://sbml.org/Facilities/Database/.
        """
        cls.i = formats.importer('sbml')
        cls.modelFour = cls.i.parse_file(os.path.join(
            DIR_FORMATS, 'sbml', '00004-sbml-l3v2-modified.xml'))

    def test_capability_reporting(self):
        """ Test if the right capabilities are reported. """
        i = formats.importer('sbml')
        self.assertTrue(i.supports_component())
        self.assertTrue(i.supports_model())
        self.assertFalse(i.supports_protocol())

    def test_model_name(self):
        """Tests whether model name is set properly."""
        name = 'case00004'
        self.assertEqual(self.modelFour.name(), name)

    def test_compartments(self):
        """
        Tests whether compartments have been imported properly. Compartments
        should include the compartments in the SBML file, plus a myokit
        compartment for the global parameters.
        """
        # compartment 1
        comp = 'compartment'
        self.assertTrue(self.modelFour.has_component(comp))

        # compartment 2
        comp = 'myokit'
        self.assertTrue(self.modelFour.has_component(comp))

        # total number of compartments
        number = 2
        self.assertEqual(self.modelFour.count_components(), number)

    def test_time(self):
        """Tests whether the time bound variable was set properly"""
        variable = 'time'
        self.assertTrue(self.modelFour.has_variable('myokit.' + variable))
        variable = self.modelFour.get('myokit.' + variable)
        self.assertTrue(variable.is_bound())

    def test_state_variables(self):
        """Tests whether all dynamic variables were imported properly."""
        # state 1
        state = 'S1'
        self.assertTrue(self.modelFour.has_variable('compartment.' + state))
        state = self.modelFour.get('compartment.' + state)
        self.assertTrue(state.is_state())

        # state 2
        state = 'S2'
        self.assertTrue(self.modelFour.has_variable('compartment.' + state))
        state = self.modelFour.get('compartment.' + state)
        self.assertTrue(state.is_state())

        # state 3
        state = 'V'
        self.assertTrue(self.modelFour.has_variable('myokit.' + state))
        state = self.modelFour.get('myokit.' + state)
        self.assertTrue(state.is_state())

        # total number of states
        number = 3
        self.assertEqual(self.modelFour.count_variables(state=True), number)

    def test_constant_parameters(self):
        """
        Tests whether all constant parameters in the file were properly
        imported.
        """
        # parameter 1
        parameter = 'k1'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 2
        parameter = 'k2'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 3
        parameter = 'size'
        self.assertTrue(
            self.modelFour.has_variable('compartment.' + parameter))
        parameter = self.modelFour.get('compartment.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 5
        parameter = 'i_Na'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 5
        parameter = 'g_Na'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 6
        parameter = 'm'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # parameter 7
        parameter = 'Cm'
        self.assertTrue(self.modelFour.has_variable('myokit.' + parameter))
        parameter = self.modelFour.get('myokit.' + parameter)
        self.assertTrue(parameter.is_constant())

        # total number of parameters
        number = 7
        self.assertEqual(self.modelFour.count_variables(const=True), number)

    def test_intermediate_parameters(self):
        """
        Tests whether all intermediate parameters in the file were properly
        imported.
        """
        # parameter 1
        parameter = 'S1_Concentration'
        self.assertTrue(
            self.modelFour.has_variable('compartment.' + parameter))
        parameter = self.modelFour.get('compartment.' + parameter)
        self.assertTrue(parameter.is_intermediary())

        # parameter 2
        parameter = 'S2_Concentration'
        self.assertTrue(
            self.modelFour.has_variable('compartment.' + parameter))
        parameter = self.modelFour.get('compartment.' + parameter)
        self.assertTrue(parameter.is_intermediary())

        # total number of parameters
        number = 2
        self.assertEqual(self.modelFour.count_variables(inter=True), number)

    def test_initial_values(self):
        """
        Tests whether initial values of constant parameters and state variables
        have been set properly.
        """
        # state 1
        state = 'S1'
        state = self.modelFour.get('compartment.' + state)
        initialValue = 0.15
        self.assertEqual(state.state_value(), initialValue)

        # state 2
        state = 'S2'
        state = self.modelFour.get('compartment.' + state)
        initialValue = 0
        self.assertEqual(state.state_value(), initialValue)

        # parameter 1
        parameter = 'k1'
        parameter = self.modelFour.get('myokit.' + parameter)
        initialValue = 0.35
        self.assertEqual(parameter.eval(), initialValue)

        # parameter 2
        parameter = 'k2'
        parameter = self.modelFour.get('myokit.' + parameter)
        initialValue = 180
        self.assertEqual(parameter.eval(), initialValue)

        # parameter 3
        parameter = 'size'
        parameter = self.modelFour.get('compartment.' + parameter)
        initialValue = 1
        self.assertEqual(parameter.eval(), initialValue)

        # parameter 4
        parameter = 'g_Na'
        parameter = self.modelFour.get('myokit.' + parameter)
        initialValue = 2
        self.assertEqual(parameter.eval(), initialValue)

        # parameter 5
        parameter = 'm'
        parameter = self.modelFour.get('myokit.' + parameter)
        initialValue = 4
        self.assertEqual(parameter.eval(), initialValue)

        # parameter 6
        parameter = 'Cm'
        parameter = self.modelFour.get('myokit.' + parameter)
        initialValue = 1
        self.assertEqual(parameter.eval(), initialValue)

    def test_rate_expressions(self):
        """
        Tests whether state variables have been assigned with the correct
        rate expression. Those may come from a rateRule or reaction.
        """
        # state 1
        state = 'S1'
        state = self.modelFour.get('compartment.' + state)
        expression = str(
            '-1 * (compartment.size * myokit.k1 * '
            + 'compartment.S1_Concentration) + compartment.size * myokit.k2'
            + ' * compartment.S2_Concentration ^ 2')
        self.assertEqual(str(state.rhs()), expression)

        # state 2
        state = 'S2'
        state = self.modelFour.get('compartment.' + state)
        expression = str(
            '2 * (compartment.size * myokit.k1 * '
            + 'compartment.S1_Concentration) - 2 * '
            + '(compartment.size * myokit.k2 '
            + '* compartment.S2_Concentration ^ 2)')
        self.assertEqual(str(state.rhs()), expression)

        # state 3
        state = 'V'
        state = self.modelFour.get('myokit.' + state)
        expression = 'myokit.i_Na / myokit.Cm'
        self.assertEqual(str(state.rhs()), expression)

    def test_assignment_rules(self):
        """
        Tests whether intermediate variables have been assigned with correct
        expressions.
        """
        # parameter 1
        parameter = 'S1_Concentration'
        parameter = self.modelFour.get('compartment.' + parameter)
        expression = 'compartment.S1 / compartment.size'
        self.assertEqual(str(parameter.rhs()), expression)

        # parameter 2
        parameter = 'S2_Concentration'
        parameter = self.modelFour.get('compartment.' + parameter)
        expression = 'compartment.S2 / compartment.size'
        self.assertEqual(str(parameter.rhs()), expression)

        # parameter 3
        parameter = 'i_Na'
        parameter = self.modelFour.get('myokit.' + parameter)
        expression = 'myokit.g_Na * myokit.m ^ 3'
        self.assertEqual(str(parameter.rhs()), expression)

    def test_units(self):
        """Tests whether units parsing."""
        # state 1
        state = 'S1'
        state = self.modelFour.get('compartment.' + state)
        unit = myokit.units.mol
        self.assertEqual(state.unit(), unit)

        # state 2
        state = 'S2'
        state = self.modelFour.get('compartment.' + state)
        unit = myokit.units.mol
        self.assertEqual(state.unit(), unit)

        # state 3
        state = 'V'
        state = self.modelFour.get('myokit.' + state)
        unit = myokit.units.V * 10 ** (-3)
        self.assertEqual(state.unit(), unit)

        # parameter 1
        parameter = 'k1'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

        # parameter 2
        parameter = 'k2'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

        # parameter 3
        parameter = 'size'
        parameter = self.modelFour.get('compartment.' + parameter)
        unit = myokit.units.L
        self.assertEqual(parameter.unit(), unit)

        # parameter 4
        parameter = 'S1_Concentration'
        parameter = self.modelFour.get('compartment.' + parameter)
        unit = myokit.units.mol / myokit.units.L
        self.assertEqual(parameter.unit(), unit)

        # parameter 5
        parameter = 'S2_Concentration'
        parameter = self.modelFour.get('compartment.' + parameter)
        unit = myokit.units.mol / myokit.units.L
        self.assertEqual(parameter.unit(), unit)

        # parameter 6
        parameter = 'i_Na'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

        # parameter 7
        parameter = 'g_Na'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

        # parameter 8
        parameter = 'm'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

        # parameter 9
        parameter = 'Cm'
        parameter = self.modelFour.get('myokit.' + parameter)
        unit = None
        self.assertEqual(parameter.unit(), unit)

    def assertBad(self, xml, message, lvl='3', v='2'):
        """
        Inserts the given ``xml`` into a <model> element, parses it, and checks
        that this raises an exception matching ``message``.
        """
        self.assertRaisesRegex(
            formats.sbml.SBMLError, message, self.parse, xml, lvl, v)

    def parse(self, xml, lvl='3', v='2'):
        """
        Inserts the given ``xml`` into a <model> element, parses it, and
        returns the result.
        """
        return self.i.parse_string(self.wrap(xml, lvl, v))

    def wrap(self, xml_content, sbml_level='3', sbml_version='2'):
        """
        Wraps xml_content into a SBML file of the specified level and
        version and returns etree root.
        """
        lvl = sbml_level
        v = sbml_version
        doc = (
            '<ns0:sbml xmlns:ns0='
            '"http://www.sbml.org/sbml/level%s/version%s/core" ' % (lvl, v)
            + 'xmlns:ns1="http://www.w3.org/1998/Math/MathML" '
            'level="%s" version="%s">\n ' % (lvl, v)
            + xml_content +
            '</ns0:sbml>')
        return doc

    def test_level_version(self):
        # Check whether error is thrown for wrong level
        self.assertBad(
            xml=' ',
            message='The file does not adhere to SBML 3.2 standards. The '
                'global namespace is not'
                ' <http://www.sbml.org/sbml/level3/version2/core>.',
            lvl=2)
        self.assertBad(
            xml=' ',
            message='The file does not adhere to SBML 3.2 standards. The '
                'global namespace is not'
                ' <http://www.sbml.org/sbml/level3/version2/core>.',
            lvl=1)

        # Check whether error is thrown for wrong version
        self.assertBad(
            xml=' ',
            message='The file does not adhere to SBML 3.2 standards. The '
                'global namespace is not'
                ' <http://www.sbml.org/sbml/level3/version2/core>.',
            v=1)

    def test_no_model(self):
        self.assertBad(
            xml=' ',
            message='The file does not adhere to SBML 3.2 standards.'
                ' No model provided.')

    def test_function_definitions(self):
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n '
            '<ns0:listOfFunctionDefinitions>\n'
            '<ns0:functionDefinition id="multiply" name="multiply">\n'
            '<ns1:math xmlns="http://www.w3.org/1998/Math/MathML">\n'
            '<lambda>\n'
            '<bvar>\n'
            '<ci> x </ci>\n'
            '</bvar>\n'
            '<bvar>\n'
            '<ci> y </ci>\n'
            '</bvar>\n'
            '<apply>\n'
            '<times/>\n'
            '<ci> x </ci>\n'
            '<ci> y </ci>\n'
            '</apply>\n'
            '</lambda>\n'
            '</ns1:math>\n'
            '</ns0:functionDefinition>\n'
            '</ns0:listOfFunctionDefinitions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='Myokit does not support functionDefinitions. Please '
            'insert your function wherever it occurs in yout SBML file and'
            ' delete the functionDefiniton in the file.')

    def test_missing_id(self):
        # missing unit ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfUnitDefinitions>\n'
            '<ns0:unitDefinition>\n'  # here is where an ID is supposed to be
            '<ns0:listOfUnits>\n'
            '<ns0:unit kind="litre" exponent="1" scale="0" multiplier="1"/>\n'
            '</ns0:listOfUnits>\n'
            '</ns0:unitDefinition>\n'
            '</ns0:listOfUnitDefinitions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No unit ID provided.')

        # missing compartment ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment/>\n'  # here is where the ID is missing
            '</ns0:listOfCompartments>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No compartment ID provided.')

        # missing parameter ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfParameters>\n'
            '<ns0:parameter/>\n'  # here is where the ID is missing
            '</ns0:listOfParameters>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No parameter ID provided.')

        # missing global conversion factor ID
        xml = (
            '<ns0:model id="test" conversionFactor="someFactor" timeUnits="s">\n'
            '<ns0:listOfParameters>\n'
            '<ns0:parameter id="someOtherFactor"/>\n'
            '</ns0:listOfParameters>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' The model conversionFactor points to non-existent ID.')

        # missing species ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species/>\n'  # here is where the ID is missing
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No species ID provided.')

        # missing conversion factor ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true" '
            'compartment="someComp" constant="false" boundaryCondition="false"'
            ' conversionFactor="someFactor"/>\n'
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' conversionFactor refers to non-existent ID.')

        # missing reactant ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction>\n'
            '<ns0:listOfReactants>\n'
            '<ns0:speciesReference species="someSpecies"/>\n'
            '</ns0:listOfReactants>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards. '
            'Species ID not existent.')

        # missing product ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction>\n'
            '<ns0:listOfProducts>\n'
            '<ns0:speciesReference species="someSpecies"/>\n'
            '</ns0:listOfProducts>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards. '
            'Species ID not existent.')

        # missing modifier ID
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true" '
            'compartment="someComp" constant="false" boundaryCondition="false"'
            '/>\n'
            '</ns0:listOfSpecies>\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction>\n'
            '<ns0:listOfReactants>\n'
            '<ns0:speciesReference species="someSpecies"/>\n'
            '</ns0:listOfReactants>\n'
            '<ns0:listOfModifiers>\n'
            '<ns0:modifierSpeciesReference species="someOtherSpecies"/>\n'
            '</ns0:listOfModifiers>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards. '
            'Species ID not existent.')

    def test_reserved_compartment_id(self):
        """
        ``MyoKit`` is a reserved ID that is used while importing for the myokit
        compartment.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="MyoKit"/>\n'
            '</ns0:listOfCompartments>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The compartment ID <MyoKit> is reserved in a myokit'
            ' import.')

    def test_reserved_parameter_id(self):
        """
        ``globalConversionFactor`` is a reserved ID that is used while
        importing the global conversion factor.
        """
        xml = (
            '<ns0:model id="test" conversionFactor="someFactor" timeUnits="s">\n'
            '<ns0:listOfParameters>\n'
            '<ns0:parameter id="globalConversionFactor"/>\n'
            '</ns0:listOfParameters>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The ID <globalConversionFactor> is protected in a myokit'
            ' SBML import. Please rename IDs.')

    def test_missing_compartment(self):
        """
        Tests whether error is thrown when ``compartment``
        attribute is not specified for a species.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies"/>\n'
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No <compartment> attribute provided.')

    def test_missing_hasOnlySubstanceUnits(self):
        """
        Tests whether error is thrown when ``hasOnlySubstanceUnits``
        attribute is not specified for a species.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" compartment="someComp"/>\n'
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No <hasOnlySubstanceUnits> flag provided.')

    def test_missing_constant(self):
        """
        Tests whether error is thrown when ``constant``
        attribute is not specified for a species.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true"'
            ' compartment="someComp"/>\n'
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No <constant> flag provided.')

    def test_missing_boundaryCondition(self):
        """
        Tests whether error is thrown when ``boundaryCondition``
        attribute is not specified for a species.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true"'
            ' compartment="someComp" constant="false"/>\n'
            '</ns0:listOfSpecies>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards.'
            ' No <boundaryCondition> flag provided.')

    def test_reserved_time_id(self):
        """
        Tests whether error is thrown when
        ``http://www.sbml.org/sbml/symbols/time`` is used as parameter or
        species ID. This is the definitionURL used by MathML to identify
        the time variable in equations. We use it as an parameter ID to
        find the time bound variable in the myokit model.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfParameters>\n'
            '<ns0:parameter id="http://www.sbml.org/sbml/symbols/time"/>\n'
            '</ns0:listOfParameters>\n'
            '</ns0:model>\n')
        time_id = 'http://www.sbml.org/sbml/symbols/time'
        self.assertBad(
            xml=xml,
            message='Using the ID <%s> for parameters or species ' % time_id
            + 'leads import errors.')

    def test_missing_reactants_products(self):
        """
        Tests whether error is thrown when reaction does neither provide
        reactants not products.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='The file does not adhere to SBML 3.2 standards. '
            'Reaction must have at least one reactant or product.')

    def test_fast_reaction(self):
        """
        Tests whether error is thrown when a reaction is flagged as ``fast``.
        Myokit treats all reactions equal, so fast reactions are not supported.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true" '
            'compartment="someComp" constant="false" boundaryCondition="false"'
            '/>\n'
            '</ns0:listOfSpecies>\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction fast="true">\n'
            '<ns0:listOfReactants>\n'
            '<ns0:speciesReference species="someSpecies"/>\n'
            '</ns0:listOfReactants>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='Myokit does not support the conversion of <fast>'
            ' reactions to steady states. Please do the maths'
            ' and substitute the steady states as AssigmentRule')

    def test_local_parameters(self):
        """
        Tests whether error is thrown when a reaction has ``localParameters``.
        Local parameters are currenly not supported in myokit.
        """
        xml = (
            '<ns0:model id="test" name="test" timeUnits="s">\n'
            '<ns0:listOfCompartments>\n'
            '<ns0:compartment id="someComp"/>\n'
            '</ns0:listOfCompartments>\n'
            '<ns0:listOfSpecies>\n'
            '<ns0:species id="someSpecies" hasOnlySubstanceUnits="true" '
            'compartment="someComp" constant="false" boundaryCondition="false"'
            '/>\n'
            '</ns0:listOfSpecies>\n'
            '<ns0:listOfReactions>\n'
            '<ns0:reaction>\n'
            '<ns0:listOfReactants>\n'
            '<ns0:speciesReference species="someSpecies"/>\n'
            '</ns0:listOfReactants>\n'
            '<ns0:kineticLaw>\n'
            '<ns0:listOfLocalParameters>\n'
            '<ns0:localParameter id="someParameter"/>'
            '</ns0:listOfLocalParameters>\n'
            '</ns0:kineticLaw>\n'
            '</ns0:reaction>\n'
            '</ns0:listOfReactions>\n'
            '</ns0:model>\n')
        self.assertBad(
            xml=xml,
            message='Myokit does currently not support the definition '
            'of local parameters in reactions. Please move '
            'their definition to the <listOfParameters> '
            'instead.')

    def test_info(self):
        i = formats.importer('sbml')
        self.assertIsInstance(i.info(), basestring)


if __name__ == '__main__':
    unittest.main()
