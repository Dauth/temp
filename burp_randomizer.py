# Burp Randomizer Extension
# Copyright 2017 Thomas Patzke <thomas@patzke.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from burp import (IBurpExtender, ISessionHandlingAction)
import re
import string
import random

### Configuration ###
# Character set of generated tokens
tokenCharset = string.ascii_letters + string.digits
tokenCharset_alpha_mixed = string.ascii_letters
tokenCharset_alpha_lower = string.ascii_lowercase
tokenCharset_alpha_upper = string.ascii_uppercase
# String which is replaced with random token
placeholder = "#RANDOM#"
placeholderNum = "#RANDOM_NUM#"
placeholderAlphaMixed = "#RANDOM_ALPHA_MIXED#"
placeholderAlphaLower = "#RANDOM_ALPHA_LOWER#"
placeholderAlphaUpper = "#RANDOM_ALPHA_UPPER#"
# Length of generated token. WARNING: length of token must equal length of placeholder due to a bug in Burp 1.5.21 which cuts off requests under certain conditions.
tokenLength = len(placeholder)
tokenLengthNum = len(placeholderNum)
#####################


class BurpExtender(IBurpExtender, ISessionHandlingAction):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Randomizer")
        self.callbacks.registerSessionHandlingAction(self)
        self.out = callbacks.getStdout()
        self.placeholder = re.compile(placeholder)
        self.placeholderNum = re.compile(placeholderNum)
        self.placeholderAlphaMixed = re.compile(placeholderAlphaMixed)
        self.placeholderAlphaLower = re.compile(placeholderAlphaLower)
        self.placeholderAlphaUpper = re.compile(placeholderAlphaUpper)
        random.seed()

    ### ISessionHandlingAction ###
    def getActionName(self):
        return "Randomizer"
    
    def performAction(self, currentRequest, macroItems):
        request = self.helpers.bytesToString(currentRequest.getRequest())
        randomToken = "".join([random.choice(tokenCharset) for i in range(tokenLength)])
        randomTokenAlphaMixed = "".join([random.choice(tokenCharset_alpha_mixed) for i in range(tokenLength)])
        randomTokenAlphaLower = "".join([random.choice(tokenCharset_alpha_lower) for i in range(tokenLength)])
        randomTokenAlphaUpper = "".join([random.choice(tokenCharset_alpha_upper) for i in range(tokenLength)])
        randomTokenNum = str(random.randint(10 ** (tokenLengthNum - 1), 10 ** (tokenLengthNum) - 1))
        request = self.placeholder.sub(randomToken, request)
        result = self.helpers.stringToBytes(self.placeholderNum.sub(randomTokenNum, request))
        result = self.helpers.stringToBytes(self.placeholderAlphaMixed.sub(randomTokenAlphaMixed, result))
        result = self.helpers.stringToBytes(self.placeholderAlphaLower.sub(randomTokenAlphaLower, result))
        result = self.helpers.stringToBytes(self.placeholderAlphaUpper.sub(randomTokenAlphaUpper, result))
        currentRequest.setRequest(result)
