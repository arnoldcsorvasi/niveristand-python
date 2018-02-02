import os

from niveristand import internal
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import Expression  # noqa: E501, I100 We need these C# imports to be out of order.
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import IfElse
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import LocalDeclaration
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import RealTimeSequence
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import ReturnDeclaration
from NationalInstruments.VeriStand.RealTimeSequenceDefinitionApi import WhileLoop
from System.IO import IOException


internal.dummy()


def add_local_variable(rt_seq, name, value):
    name = _create_unique_lv_name(name)
    local_declaration = LocalDeclaration(name, value._data_value)
    rt_seq.Variables.LocalVariables.AddLocalVariable(local_declaration)
    return name


def add_assignment(block, dest_name, source_name):
    add_expression(block, '%s = %s' % (dest_name, source_name))


def add_expression(block, expression):
    block.AddStatement(Expression('%s' % expression))


def add_if_else(block, test_condition):
    if_else = IfElse(Expression(test_condition))
    block.AddStatement(if_else)
    return if_else


def add_while(block, test_condition):
    while_block = WhileLoop(Expression(test_condition), False)
    block.AddStatement(while_block)
    return while_block


def create_real_time_sequence():
    return RealTimeSequence()


def add_return_variable(rtseq, name, default_value):
    name = _create_unique_lv_name(name)
    return_declaration = ReturnDeclaration(name, default_value._data_value)
    rtseq.Variables.ReturnType = return_declaration
    return name


def save_real_time_sequence(rtseq, filepath):
    try:
        rtseq.SaveSequence(os.path.join(filepath))
    except(IOException) as e:
        raise IOError(e.Message)


def _create_unique_lv_name(name):
    try:
        _create_unique_lv_name.lv_cnt += 1
    except AttributeError:
        _create_unique_lv_name.lv_cnt = 0
    if name is None:
        name = ''
    name = 'lv_' + name + '_' + str(_create_unique_lv_name.lv_cnt)
    _create_unique_lv_name.lv_cnt += 1
    return name


def to_channel_ref_name(name):
    return "ch_" + name
