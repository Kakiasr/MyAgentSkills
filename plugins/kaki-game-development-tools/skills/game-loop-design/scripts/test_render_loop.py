"""Regression checks for four-type nodes and separately scoped information."""
import copy
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from render_loop import render


def specimen():
    return {
        "width":1000,"height":700,"start":"act",
        "loops":[
            {"id":"main","label":"主循环","x":250,"y":350,"width":460,"height":660,"global_information":["coins"]},
            {"id":"child","label":"子循环","x":750,"y":350,"width":460,"height":660,"global_information":["coins_child"]}],
        "nodes":[
            {"id":"coins","label":"当前金币","kind":"information","loop":"main","x":250,"y":140},
            {"id":"coins_child","label":"当前金币","kind":"information","loop":"child","x":750,"y":140},
            {"id":"act","label":"采取行动","kind":"action","loop":"main","x":150,"y":340,"width":140},
            {"id":"sub","label":"子循环","kind":"subloop","loop":"main","loop_ref":"child","x":350,"y":340,"width":140},
            {"id":"child_act","label":"作出选择","kind":"action","loop":"child","x":750,"y":340},
            {"id":"result","label":"选择结果","kind":"information","loop":"child","x":750,"y":500}],
        "edges":[{"from":"act","to":"sub"},{"from":"sub","to":"child_act"},
                 {"from":"child_act","to":"result"},
                 {"from":"result","to":"act","via":[[750,610],[150,610]]}]}


class RenderLoopTests(unittest.TestCase):
    def test_scoped_information_is_not_unreachable(self):
        data=specimen(); before=copy.deepcopy(data)
        svg,mmd,report=render(data)
        ET.fromstring(svg)
        self.assertEqual(report['warnings'],[])
        self.assertEqual(report['loop_bodies'],2)
        self.assertEqual(report['global_information_nodes'],['coins','coins_child'])
        self.assertEqual(svg.count('全局可获取信息'),2)
        self.assertIn('subgraph G_child',mmd)
        self.assertIn('fill:#eae1fc',mmd)
        self.assertEqual(data,before)

    def test_four_types_and_example(self):
        data=json.loads((Path(__file__).resolve().parents[1]/'examples/five-step-loop.json').read_text(encoding='utf-8'))
        _,_,report=render(data)
        self.assertEqual(report['warnings'],[])
        self.assertEqual(len(report['global_information_nodes']),4)
        data=specimen();data['nodes'][2]['kind']='branch'
        _,_,report=render(data)
        self.assertTrue(any('labeled outcome' in w for w in report['warnings']))

    def test_legacy_types_rejected(self):
        for kind in ['step','decision','terminal','event','state']:
            with self.subTest(kind=kind):
                data=specimen();data['nodes'][2]['kind']=kind
                with self.assertRaises(ValueError):render(data)

    def test_global_information_cannot_be_a_flow_step(self):
        for edge in [{'from':'act','to':'coins'},{'from':'coins','to':'act'}]:
            data=specimen();data['edges'].append(edge)
            with self.assertRaises(ValueError):render(data)

    def test_each_loop_requires_own_information_scope(self):
        for mutate in [lambda d:d['loops'][1].pop('global_information'),
                       lambda d:d['loops'][1].update(global_information=['coins']),
                       lambda d:d['loops'][1].update(global_information=[])]:
            data=specimen();mutate(data)
            with self.assertRaises(ValueError):render(data)

    def test_unknown_or_noninformation_scope_rejected(self):
        for bad in ['missing','act']:
            data=specimen();data['loops'][0]['global_information']=[bad]
            with self.assertRaises(ValueError):render(data)

    def test_explicit_empty_scope(self):
        data=specimen();data['loops'][1].update(global_information=[],global_information_note='无')
        data['nodes']=[n for n in data['nodes'] if n['id']!='coins_child']
        svg,mmd,report=render(data)
        self.assertIn('全局可获取信息：无',svg)
        self.assertIn('G_child_note',mmd)
        self.assertEqual(report['warnings'],[])

    def test_loop_ownership_and_subloop_reference(self):
        for field,value in [('loop','missing'),('loop_ref','missing')]:
            data=specimen();data['nodes'][3][field]=value
            with self.assertRaises(ValueError):render(data)

    def test_global_information_not_a_start(self):
        data=specimen();data['start']='coins'
        with self.assertRaises(ValueError):render(data)


if __name__=='__main__':
    unittest.main()
