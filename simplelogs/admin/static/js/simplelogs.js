'use strict';

var Simplelogs = angular.module('Simplelogs', [
    'hitsl',
    'ui.bootstrap',
    'ui.select',
    'ngSanitize'
])
.config(['$interpolateProvider', 'paginationConfig', 'datepickerConfig', 'datepickerPopupConfig',
        function ($interpolateProvider, paginationConfig, datepickerConfig, datepickerPopupConfig) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
    paginationConfig.firstText = 'Первая';
    paginationConfig.lastText = 'Последняя';
    paginationConfig.previousText = 'Предыдущая';
    paginationConfig.nextText = 'Следующая';
    datepickerConfig.showWeek = false;
    datepickerConfig.startingDay = 1;
    datepickerPopupConfig.currentText = 'Сегодня';
    datepickerPopupConfig.toggleWeeksText = 'Недели';
    datepickerPopupConfig.clearText = 'Убрать';
    datepickerPopupConfig.closeText = 'Готово';
}])
.filter('asDateTime', function ($filter) {
    return function (data) {
        if (!data) return data;
        var result = moment(data);
        if (!result.isValid()) return data;
        return result.format('DD.MM.YYYY HH:mm');
    }
})
.filter('asDate', function ($filter) {
    return function (data) {
        if (!data) return data;
        var result = moment(data);
        if (!result.isValid()) return data;
        return result.format('DD.MM.YYYY');
    }
})
;


Simplelogs
.controller('JournalListCtrl', ['$scope', '$modal', 'SimplelogsApi', function ($scope, $modal, SimplelogsApi) {
    var logEntryViewModalConfig = {
        controller: 'LogEntryViewModalCtrl',
        templateUrl: '/Simplelogs/modal/log_entry_view.html',
        size: 'lg',
        backdrop: 'static',
        resolve: {}
    };
    $scope.pager = {
        current_page: 1,
        per_page: 10,
        max_pages: 15,
        pages: null,
        record_count: null
    };
    $scope.item_list = [];
    $scope.flt = {
        enabled: true,
        model: {}
    };
    $scope.owner_systems = [];
    $scope.log_levels = [];
    $scope.tags = [];

    $scope.openView = function (idx) {
        var item = _.deepCopy($scope.item_list[idx]);
        logEntryViewModalConfig.resolve.model = function () {
            return item;
        };
        return $modal.open(logEntryViewModalConfig).result;
    };
    $scope.toggleFilter = function () {
        $scope.flt.enabled = !$scope.flt.enabled;
    };
    $scope.isFilterEnabled = function () {
        return $scope.flt.enabled;
    };
    $scope.clear = function () {
        $scope.flt.model = {};
    };
    $scope.clearAll = function () {
        $scope.clear();
        $scope.pager.current_page = 1;
        $scope.pager.pages = null;
        $scope.pager.record_count = null;
        $scope.item_list = [];
    };
    $scope.getData = function () {
        $scope.pager.current_page = 1;
        $scope.refreshData();
    };

    var setData = function (paged_data) {
        $scope.item_list = paged_data.items;
        $scope.pager.record_count = paged_data.count;
        $scope.pager.pages = paged_data.total_pages;
    };
    $scope.refreshData = function () {
        var args = {
            skip: ($scope.pager.current_page - 1) * $scope.pager.per_page,
            limit: $scope.pager.per_page,
            flt: angular.toJson({
                data: $scope.flt.model.text || undefined,
                start: $scope.flt.model.date_from !== undefined ?
                    moment($scope.flt.model.date_from).startOf('day').format('YYYY-MM-DD HH:mm:ss') :
                    undefined,
                end: $scope.flt.model.date_to !== undefined ?
                    moment($scope.flt.model.date_to).endOf('day').format('YYYY-MM-DD HH:mm:ss') :
                    undefined,
                owner: $scope.flt.model.owner_system || undefined,
                level: $scope.flt.model.level || undefined,
                tags: $scope.flt.model.tags && $scope.flt.model.tags.length ?
                    $scope.flt.model.tags :
                    undefined
            })
        };
        SimplelogsApi.log_entries.get_list(args).then(setData);
    };
    $scope.onPageChanged = function () {
        $scope.refreshData();
    };
    $scope.getRowClass = function (item) {
        var c = [];
        if (item.level === 'error' || item.level === 'critical') c.push('bg-danger');
        if (item.level === 'warning') c.push('bg-warning');
        if (item.level === 'info' || item.level === 'notice') c.push('bg-info');
        return c;
    };

    $scope.init = function () {
        SimplelogsApi.misc.get_owners().then(function (data) {
            $scope.owner_systems = data;
        });
        SimplelogsApi.misc.get_log_levels().then(function (data) {
            $scope.log_levels = data.level;
        });
        SimplelogsApi.misc.get_tags().then(function (data) {
            $scope.tags = data;
        });

        $scope.refreshData();
    };

    $scope.init();
}])
.controller('LogEntryViewModalCtrl', ['$scope', 'model',
    function ($scope, model) {
        $scope.model = model;
}])
.run(['$templateCache', function ($templateCache) {
    $templateCache.put(
        '/Simplelogs/modal/log_entry_view.html',
        '\
<div class="modal-header" xmlns="http://www.w3.org/1999/html">\
    <button type="button" class="close" ng-click="$dismiss()">&times;</button>\
    <h4 class="modal-title">Запись лога</h4>\
</div>\
<div class="modal-body">\
<form class="form-horizontal">\
<div class="row">\
    <div class="col-md-6">\
        <div class="form-group">\
            <label for="system" class="col-sm-3 control-label">Подсистема</label>\
            <div class="col-sm-9">\
                <div class="form-control-static" id="system">\
                    <b>version: </b>[[ model.owner.version ]]<br><b>name: </b>[[ model.owner.name ]]\
                </div>\
            </div>\
        </div>\
    </div>\
\
    <div class="col-md-6">\
        <div class="form-group">\
            <label for="date" class="col-sm-3 control-label">Дата</label>\
            <div class="col-sm-9">\
                <div class="form-control-static" id="date" ng-bind="model.datetimestamp | asDateTime"></div>\
            </div>\
        </div>\
    </div>\
</div>\
\
<div class="row">\
    <div class="col-md-6">\
        <div class="form-group">\
            <label for="level" class="col-sm-3 control-label">Уровень</label>\
            <div class="col-sm-9">\
                <div class="form-control-static" id="level" ng-bind="model.level"></div>\
            </div>\
        </div>\
    </div>\
\
    <div class="col-md-6">\
        <div class="form-group">\
            <label for="tags" class="col-sm-3 control-label">Теги</label>\
            <div class="col-sm-9">\
                <div class="form-control-static" id="tags">\
                    <span ng-repeat="tag in model.tags">[[ tag ]]</span>\
                </div>\
            </div>\
        </div>\
    </div>\
</div>\
\
<div class="row">\
    <div class="col-md-12">\
        <textarea ng-model="model.data" rows="10" class="form-control" readonly></textarea>\
    </div>\
</div>\
\
</form>\
</div>\
<div class="modal-footer">\
    <button type="button" class="btn btn-default" ng-click="$dismiss()">Закрыть</button>\
</div>');
}])
;


Simplelogs
.service('SimplelogsApi', ['$q', 'NotificationService', 'ApiCalls',
        function ($q, NotificationService, ApiCalls) {
    var self = this;
    this.log_entries = {
        get_list: function (args) {
            return ApiCalls.wrapper('GET', 'api/0/log_entries', args);
        }
    };

    this.misc = {
        get_owners: function () {
            return ApiCalls.wrapper('GET', '/api/owners/');
        },
        get_log_levels: function () {
            return ApiCalls.wrapper('GET', '/api/level/');
        },
        get_tags: function () {
            return ApiCalls.wrapper('GET', '/api/tags');
        }
    };
}]);
