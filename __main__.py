"""
 * Copyright (c) 2020 Den Zemtcov <dlya.v5ego@yandex.com>

 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 * The above copyright notice and this permission notice (including the next
 * paragraph) shall be included in all copies or substantial portions of the
 * Software.
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
"""

import sys

# GDB commands translation between MI and interactive interface
#
# Implement a python class with a `TranslateBreakpointCommand` method, which would translate the following GDB interactive commands to their MI counterparts:
#
# * `ignore` to `-break-after`
# * `commands` to `-break-commands`
# * `condition` to `-break-condition`
#
# Additional requirements:
#
# * Please implement the class in such a way, that it can be extended to support additional command translation.
# * Please supply the implemented class with tests.
#
# Please refer to <https://sourceware.org/gdb/onlinedocs/gdb/GDB_002fMI-Breakpoint-Commands.html> for command details.
# Usage example:
# TranslateBReakpointCommand("ignore 1 2") == "-break-after 1 2"
class GDBTranslator:
    def TranslateBreakpointCommand(self, command):
        com = command.split(" ")
        if com[0] == 'ignore':
            result_com = '-break-after'
            com.remove('ignore')
            result_com += ' ' + " ".join(com)
        elif com[0] == 'commands':
            result_com = '-break-commands'
            com.remove('commands')
            result_com += ' ' + " ".join(com)
        elif com[0] == 'condition':
            result_com = '-break-condition'
            com.remove('condition')
            result_com += ' ' + " ".join(com)
        else:
            result_com = 'Error : Command not released'
        return result_com
# =========================================================================
# App trace analyser with events
#
# Given input sequence of application trace tokens of the following format:
#
# `PUSH:TID:TIME:MESSAGE`, `POP:TID:TIME`, `EVENT:TID:TIME:MESSAGE` where:
#
# * PUSH indicates opening a new range.
# * POP indicates closing the last opened range.
# * EVENT indicates, that an event, which context must be captures, has occured.
# * TID is thread id. All ranges are local to a single thread.
# * TIME is time. Input token sequence is sorted by this field.
# * Message is an arbitrary string.
#
# For each event return a list of ranges, opened in the thread, where event has occured at the time of the event, sorted by the event time.
#
#
# For example, consider the following sequence:
#
# * `PUSH:1:100:Open 1` - start range with message "Open 1" in thread 1
# * `EVENT:1:120:Event 1` - event with message "Event 1" has occured in theread 1
# * `PUSH:1:200:Open 2` - start range with message "Open 2" in thread 1
# * `EVENT:1:220:Event 2` - event with message "Event 2" has occured in theread 1
# * `POP:1:300` - close last range ("Open 2") in thread 1
# * `PUSH:2:400:Open 3` - start range with message "Open 3" in thread 2
# * `EVENT:2:450:Event 3` - event with message "Event 3" has occured in theread 2
# * `POP:1:500` - close range ("Open 1") in thread 1
# * `POP:2:600` - close range ("Open 3") in thread 2
#
# The following list must be returned:
#
# [("Event 1", ["Open 1"]), ("Event 2", ["Open 1", "Open 2"]), ("Event 3", ["Open 3"])]
#
# Please provide tests for your implementation.
#
# Usage example:
# % trace = ["PUSH:1:100:Open 1", "EVENT:1:120:Event 1", "PUSH:1:200:Open 2", "EVENT:1:220:Event 2", "POP:1:300", "PUSH:2:400:Open 3", "EVENT:2:450:Event 3", "POP:1:500", "POP:2:600"]
# % ret = ProcessAppTraceWithEvents(trace)
# % ret == [("Event 1", ["Open 1"]), ("Event 2", ["Open 1", "Open 2"]), ("Event 3", ["Open 3"])]


def ProcessAppTraceWithEvents(trace):
    thread_token_list = {}
    return_list = {}
    for i in range(0, len(trace)):
        token_list = trace[i].split(':')
        if token_list[0] == 'PUSH':
            thread_token_list.setdefault(token_list[1], []).append(token_list[3])
        elif token_list[0] == 'POP':
            thread_token_list[token_list[1]].pop()
        elif token_list[0] == 'EVENT':
            res = thread_token_list.get(token_list[1])
            return_list.setdefault(token_list[3], []).extend(res)
    return return_list

# =========================================================================
# Compiler output processing
#
# Write a python function which takes model compiler output as an input and outputs error statistics.
#
# First argument is a list of strings of the following format:
#
#  `filename:line error (code)'
#
#  For example:
#
#  "a/b/main.c:12 Invalid variable reference (123)"
#
# Second argument is one of the following strings:
#   * "first": Function should return a list of strings indicating the first error in each file which contains error. Note, that input lines might not be sorted.
#   * "total": Function should return a list of strings indicating the total number of errors in each file.
#   * "code": Function shodul return a list of all filenames and lines with the given error code (supplied via named argument CODE).
#   * Error message should be printed in all other cases.
#
# For example:
# % input = ["a/b.c:12 Invalid jump (12)", "a/d.c:98 Multiple gotos (45)", "a/b.c:3 Undefined variable (05)"]
# % out1 = ProcessOutput(input, "first")
# % out1 == ["a/b.c Undefined variable (05)", "a/d.c Multiple gotos (45)"]
# % out2 = ProcessOutput(input, "total")
# % out2 == ["a/b.c:2", "a/d.c:1"]
# % out3 = ProcessOutput(input, "code", CODE = 12)
# % out3 == "a/b.c:12"
#
# Hint you might need to change the function declarataion.
# Please provide tests with your implementation.

def ProcessOutput(input, mode):
    pass

def test_translate_breakpoint_command():
    testObj = GDBTranslator()
    string_res = testObj.TranslateBreakpointCommand("ignore 1 2")
    print(string_res)
    string_res = testObj.TranslateBreakpointCommand("commands 1 print v continue")
    print(string_res)
    string_res = testObj.TranslateBreakpointCommand("condition 1 1")
    print(string_res)

def test_process_app_trace():
    trace = ["PUSH:1:100:Open 1", "EVENT:1:120:Event 1", "PUSH:1:200:Open 2",
             "EVENT:1:220:Event 2", "POP:1:300", "PUSH:2:400:Open 3",
             "EVENT:2:450:Event 3", "POP:1:500", "POP:2:600"]

    ret = ProcessAppTraceWithEvents(trace)
    print(ret)

def test_process_output():
    pass

def main(argv):
    #test_translate_breakpoint_command()
    test_process_app_trace()
    #test_process_output()

if __name__ == '__main__':
    main(sys.argv)