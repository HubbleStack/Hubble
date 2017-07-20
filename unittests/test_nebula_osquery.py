import pytest
import yaml
import hubblestack.extmods.modules.nebula_osquery

class TestNebula():

    def test__virtual__(self):
        var = hubblestack.extmods.modules.nebula_osquery.__virtual__()
        assert var == 'nebula'

    def test_version(self):
        var = hubblestack.extmods.modules.nebula_osquery.version()
        assert var == '2.1.7'

    def test_hubble_versions(self):
        var = hubblestack.extmods.modules.nebula_osquery.hubble_versions()
        assert ((var.get('hubble_versions')).get('result')) == True

    def test_queries_query_grp_day(self):
        query_group = 'day'
        query_file = '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        def cp_cache_file(queryFile):
            return '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        __salt__ = {}
        __salt__['cp.cache_file'] = cp_cache_file
        hubblestack.extmods.modules.nebula_osquery.__salt__ = __salt__
        def cmd_run_all(cmd):
            return {'retcode': 0, 'pid': 3478, 'stdout': '[{"build":"","codename":"xenial","major":"16","minor":"4","name":"Ubuntu","patch":"","platform":"ubuntu","platform_like":"debian","query_time":"1500395829","version":"16.04.2 LTS (Xenial Xerus)"}]', 'stderr': ''}
        __salt__['cmd.run_all'] = cmd_run_all
        hubblestack.extmods.modules.nebula_osquery.__salt__ = __salt__
        var = hubblestack.extmods.modules.nebula_osquery.queries(query_group, query_file,verbose=False,report_version_with_day=True)
        hubblestack.extmods.modules.nebula_osquery.__salt__ = {}
        assert var != 0

    def test_queries_query_grp_hour(self):
        query_group = 'fifteen_min'
        query_file = '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        def cp_cache_file(queryFile):
            return '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        __salt__ = {}
        __salt__['cp.cache_file'] = cp_cache_file
        hubblestack.extmods.modules.nebula_osquery.__salt__ = __salt__
        def cmd_run_all(cmd):
            return {'retcode': 0, 'pid': 3478, 'stdout': '[{"build":"","codename":"xenial","major":"16","minor":"4","name":"Ubuntu","patch":"","platform":"ubuntu","platform_like":"debian","query_time":"1500395829","version":"16.04.2 LTS (Xenial Xerus)"}]', 'stderr': ''}
        __salt__['cmd.run_all'] = cmd_run_all
        var = hubblestack.extmods.modules.nebula_osquery.queries(query_group, query_file,verbose=False,report_version_with_day=True)
        assert var != 0

    def test_queries_for_report_version_with_day(self):
        query_group = 'day'
        query_file = '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        def cp_cache_file(queryFile):
            return '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        __salt__ = {}
        __salt__['cp.cache_file'] = cp_cache_file
        hubblestack.extmods.modules.nebula_osquery.__salt__ = __salt__
        def cmd_run_all(cmd):
            return {'retcode': 0, 'pid': 3478, 'stdout': '[{"build":"","codename":"xenial","major":"16","minor":"4","name":"Ubuntu","patch":"","platform":"ubuntu","platform_like":"debian","query_time":"1500395829","version":"16.04.2 LTS (Xenial Xerus)"}]', 'stderr': ''}
        __salt__['cmd.run_all'] = cmd_run_all
        var = hubblestack.extmods.modules.nebula_osquery.queries(query_group, query_file,verbose=False,report_version_with_day=False)
        assert var != 0

    def test_queries_query_grp_hour(self):
        query_group = 'hour'
        query_file = '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        def cp_cache_file(queryFile):
            return '/root/myhubblefiles/hubblestack_nebula_queries.yaml'
        __salt__ = {}
        __salt__['cp.cache_file'] = cp_cache_file
        hubblestack.extmods.modules.nebula_osquery.__salt__ = __salt__
        def cmd_run_all(cmd):
            return {'retcode': 0, 'pid': 3478, 'stdout': '[{"build":"","codename":"xenial","major":"16","minor":"4","name":"Ubuntu","patch":"","platform":"ubuntu","platform_like":"debian","query_time":"1500395829","version":"16.04.2 LTS (Xenial Xerus)"}]', 'stderr': ''}
        __salt__['cmd.run_all'] = cmd_run_all
        var = hubblestack.extmods.modules.nebula_osquery.queries(query_group, query_file,verbose=False,report_version_with_day=True)
        assert var != 0


