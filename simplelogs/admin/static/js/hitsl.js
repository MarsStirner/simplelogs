/**
 * Created by mmalkov on 19.03.15.
 */


angular.module('hitsl', [])
.config(function ($httpProvider) {
    $httpProvider.interceptors.push('requestInterceptor');
})
.factory('requestInterceptor', function ($q, $rootScope) {
    $rootScope.pendingRequests = 0;
    return {
        'request': function (config) {
            if (!config.silent) {
                $rootScope.pendingRequests++;
            }
            return config || $q.when(config);
        },

        'requestError': function(rejection) {
            if (!safe_traverse(rejection, 'silent')) {
                $rootScope.pendingRequests--;
            }
            return $q.reject(rejection);
        },

        'response': function(response) {
            if (!response.config.silent) {
                $rootScope.pendingRequests--;
            }
            return response || $q.when(response);
        },

        'responseError': function(rejection) {
            if (!rejection.config.silent) {
                $rootScope.pendingRequests--;
            }
            return $q.reject(rejection);
        }
    }
})
.service('ApiCalls', ['$q','$http', 'NotificationService', function ($q, $http, NotificationService) {
    this.wrapper = function (method, url, params, data, options) {
        if (options === undefined) options = {};
        var defer = $q.defer();
        function process(response) {
            if (response.status >= 400 || response.data.meta.code >= 400) {
                var text = (response.status === 500) ? 'Внутренняя ошибка сервера.<br/>{0}' : 'Ошибка.<br/>{0}';
                NotificationService.notify(
                    response.data.meta.code,
                    text.format(response.data.meta.name),
                    'danger'
                );
                defer.reject(response.data.meta);
            } else {
                defer.resolve(response.data.result);
            }
            return response;
        }
        $http(angular.extend({}, options, {
            method: method,
            url: url,
            params: params,
            data: data,
            headers: {
                'X-Requested-With' :'XMLHttpRequest'
            }
        }))
        .then(process, process);
        return defer.promise;
    };
}])
.service('NotificationService', ['TimeoutCallback', function (TimeoutCallback) {
    var self = this;
    var recompilers = [];
    this.notifications = [];
    this.timeouts = {};
    this.notify = function (code, message, severity, to) {
        if (to === true) to = 3000;
        else if (!angular.isNumber(to)) to = undefined;
        var id = Math.floor(Math.random() * 65536);
        self.notifications.unshift({
            id: id,
            code: code,
            message: message,
            severity: severity,
            to: to
        });
        if (to) {
            this.timeouts[id] = new TimeoutCallback(_.partial(this.dismiss, id), to);
            this.timeouts[id].start();
        }
        notify_recompilers();
        return id;
    };
    this.dismiss = function (id) {
        self.notifications = self.notifications.filter(function (notification) {
            return notification.id != id;
        });
        notify_recompilers();
    };
    this.cancelTO = function (id) {
        this.timeouts[id].kill();
    };
    this.register = function (recompile_function) {
        recompilers.push(recompile_function);
    };
    var notify_recompilers = function () {
        recompilers.forEach(function (recompile) {
            recompile(self.notifications);
        });
    }
}])
.directive('alertNotify', function (NotificationService, $compile) {
    return {
        restrict: 'AE',
        scope: {},
        link: function (scope, element, attributes) {
            var template =
                '<div class="alert alert-{0} novmargin" role="alert" {3}>\
                    <button type="button" class="close" ng-click="$dismiss({2})">\
                        <span aria-hidden="true">&times;</span>\
                        <span class="sr-only">Close</span>\
                    </button>\
                    <span style="margin-right: 10px">{1}</span>\
                </div>';
            scope.$dismiss = function (id) {
                NotificationService.dismiss(id);
            };
            function compile (arg) {
                var _arg = _(arg);
                if (_.isArray(arg)) {
                    return arg.map(compile).join('');
                } else if (typeof arg === 'string') {
                    return arg;
                } else if (typeof arg !== 'object') {
                    return '';
                }
                var wrapper = '{0}';
                if (_arg.has('bold') && arg.bold) {
                    wrapper = '<b>{0}</b>'.format(wrapper)
                }
                if (_arg.has('italic') && arg.bold) {
                    wrapper = '<i>{0}</i>'.format(wrapper)
                }
                if (_arg.has('underline') && arg.bold) {
                    wrapper = '<u>{0}</u>'.format(wrapper)
                }
                if (_arg.has('link')) {
                    //noinspection HtmlUnknownTarget
                    wrapper = '<a href="{0}">{1}</a>'.format(arg.link, wrapper);
                } else if (_arg.has('click')) {
                    do {
                        var uniq = _.random(0x100000000);
                    } while (scope.func_map.hasOwnProperty(uniq));
                    scope.func_map[uniq] = arg.click;
                    wrapper = '<a style="cursor:pointer" ng-click="func_map[{0}]()">{1}</a>'.format(String(uniq), wrapper)
                }
                if (_arg.has('text')) {
                    return wrapper.format(compile(arg.text));
                }
                return '';
            }
            function recompile (n) {
                scope.func_map = {};
                var html = n.map(function (notification) {
                    return template.format(
                        notification.severity || 'info',
                        compile(notification.message),
                        notification.id,
                        notification.to ? 'ng-mouseover="onMouseOver({0})"'.format(notification.id): ''
                    )
                }).join('\n');
                var replace_element = $('<div class="abs-alert">{0}</div>'.format(html));
                element.replaceWith(replace_element);
                $compile(replace_element)(scope);
                element = replace_element;
            }
            NotificationService.register(recompile);
            scope.onMouseOver = function (id) {
                NotificationService.cancelTO(id);
            };
        }
    }
})
.factory('TimeoutCallback', ['$timeout', '$interval', function ($timeout, $interval) {
    var Timeout = function (callback, timeout) {
        this.timeout = timeout;
        this.hideki = null;
        this.interval_promise = null;
        this.callback = callback;
    };
    Timeout.prototype.kill = function () {
        if (this.hideki) {
            $timeout.cancel(this.hideki);
            this.hideki = null;
        }
        if (this.interval_promise) {
            $interval.cancel(this.interval_promise);
            this.interval_promise = null;
        }
        return this;
    };
    Timeout.prototype.start = function (timeout) {
        this.kill();
        if (timeout !== undefined) {
            this.timeout = timeout;
        }
        this.hideki = $timeout(this.callback, this.timeout);
        return this;
    };
    Timeout.prototype.start_interval = function (count, timeout) {
        this.kill();
        if (timeout !== undefined) {
            this.timeout = timeout;
        }
        this.interval_promise = $interval(this.callback, this.timeout, count || 0, false);
        return this;
    };
    return Timeout;
}])
.directive('simpleCollapsable', [function () {
    return {
        restrict: 'AEC',
        scope: {},
        transclude: true,
        template:
'<div ng-class="{\'simple-collapsed\': collapsed}" style="position: relative;">\
    <div ng-transclude></div>\
    <div style="height: 15px;"></div>\
    <div style="height: 15px; position: absolute; bottom:0; width: 100%;\
         background: linear-gradient(rgba(255, 255, 255, 0), rgba(255, 255, 255, 1));"\
         ng-show="controlVisible()">\
        <div style="position:relative; width: 100%; height: 100%;">\
            <a style="position:absolute; bottom: 0; right: 0;" href="javascript:void(0);" ng-click="collapsed=!collapsed"\
                ng-show="collapsed">[ Развернуть ]</a>\
            <a style="position:absolute; bottom: 0; right: 0;" href="javascript:void(0);" ng-click="collapsed=!collapsed"\
                ng-show="!collapsed">[ Свернуть ]</a>\
        </div>\
    </div>\
</div>',
        link: function (scope, element, attributes) {
            scope.collapsed = true;
            scope.controlVisible = function () {
                return element.height() >= 60;
            };
        }
    }
}])
.directive('wmDate', ['$timeout', '$compile', function ($timeout, $compile) {
    return {
        restrict: 'E',
        require: '^ngModel',
        link: function (original_scope, element, attrs, ngModelCtrl) {
            var scope = original_scope.$new(false);
            scope.popup = { opened: false };
            scope.open_datepicker_popup = function (prev_state) {
                $timeout(function () {
                    scope.popup.opened = !prev_state;
                    if (!ngModelCtrl.$modelValue) {
                        ngModelCtrl.$setViewValue(new Date().toISOString().slice(0, 10));
                    }
                });
            };
            var _id = attrs.id,
                name = attrs.name,
                ngDisabled = attrs.ngDisabled,
                ngRequired = attrs.ngRequired,
                ngModel = attrs.ngModel,
                style = attrs.style,
                minDate = attrs.minDate,
                maxDate = attrs.maxDate,
                autofocus = attrs.autofocus;
            var wmdate = $('<div class="input-group"></div>'),
                date_input = $('\
                    <input type="text" class="form-control" autocomplete="off" datepicker_popup="dd.MM.yyyy"\
                        is-open="popup.opened" manual-date ui-mask="99.99.9999" date-mask />'
                ),
                button = $('\
                    <button type="button" class="btn btn-default" ng-click="open_datepicker_popup(popup.opened)">\
                        <i class="glyphicon glyphicon-calendar"></i>\
                    </button>'
                ),
                button_wrap = $('<span class="input-group-btn"></span>');
            if (_id) date_input.attr('id', _id);
            if (name) date_input.attr('name', name);
            date_input.attr('ng-model', ngModel);
            if (ngDisabled) {
                date_input.attr('ng-disabled', ngDisabled);
                button.attr('ng-disabled', ngDisabled);
            }
            if (autofocus){
                date_input.attr('auto-focus', '');
            }
            if (style) {
                wmdate.attr('style', style);
                element.removeAttr('style');
            }
            if (ngRequired) date_input.attr('ng-required', ngRequired);
            if (!minDate) {
                scope.__mindate = new Date(1900, 0, 1);
                minDate = '__mindate';
            }
            date_input.attr('min', minDate);
            if (maxDate) date_input.attr('max', maxDate);

            button_wrap.append(button);
            wmdate.append(date_input, button_wrap);
            $(element).append(wmdate);
            $compile(wmdate)(scope);
        }
    };
}])
.directive('manualDate', [function() {
    return {
        restrict: 'A',
        require: '^ngModel',
        link: function(scope, elm, attrs, ctrl) {
            ctrl.$parsers.unshift(function(_) {
                var viewValue = ctrl.$viewValue,
                    maxDate = scope.$eval(attrs.max),
                    minDate = scope.$eval(attrs.min);
                if (!viewValue || viewValue instanceof Date) {
                    return viewValue;
                }
                var d = moment(viewValue.replace('_', ''), "DD.MM.YYYY", true);
                if (moment(d).isValid() &&
                        (maxDate ? moment(maxDate).isAfter(d) : true) &&
                        (minDate ? moment(minDate).isBefore(d) || moment(minDate).isSame(d) : true)) {
                    ctrl.$setValidity('date', true);
                    ctrl.$setViewValue(d.toDate());
                    return d;
                } else {
                    ctrl.$setValidity('date', false);
                    return undefined;
                }
            });
        }
    };
}])
;


// Convenience

function safe_traverse(object, attrs) {
    var o = object,
        attr,
        default_val = arguments[2];
    for (var i = 0; i < attrs.length; ++i) {
        attr = attrs[i];
        o = o[attr];
        if (o === undefined || (o === null && i < attrs.length - 1)) {
            return default_val;
        }
    }
    return o;
}

function indexOf(array, elem) {
  var index, _i, _ref;
  for (index = _i = 0, _ref = array.length - 1; 0 <= _ref ? _i <= _ref : _i >= _ref; index = 0 <= _ref ? ++_i : --_i) {
    if (angular.equals(array[index], elem)) {
      return index;
    }
  }
  return -1;
}

// String.prototype
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}
if (!String.prototype.formatNonEmpty) {
    String.prototype.formatNonEmpty = function() {
        var args = arguments;
        return this.replace(/{([\w\u0400-\u04FF\s\.,</>()]*)\|?(\d+)\|?([\w\u0400-\u04FF\s\.,</>()]*)}/g, function(match, prefix, number, suffix) {
            return typeof args[number] != 'undefined'
                ? (args[number] ? (prefix + args[number] + suffix): '')
                : ''
                ;
        });
    };
}
if (!String.prototype.startswith) {
    String.prototype.startswith = function (prefix) {
        return this.indexOf(prefix) === 0;
    }
}
if (!String.prototype.endswith) {
    String.prototype.endswith = function (suffix) {
        return this.indexOf(suffix, this.length - suffix.length) !== -1;
    }
}
if (!String.prototype.contains) {
    String.prototype.contains = function (infix) {
        return this.indexOf(infix) !== -1;
    }
}

// Array.prototype
if (!Array.prototype.clone) {
    Array.prototype.clone = function () {
        var b = [];
        var i = this.length;
        while (i--) {b[i] = this[i]}
        return b;
    }
}
if (!Array.prototype.has) {
    Array.prototype.has = function (item) {
        return this.indexOf(item) !== -1
    }
}
if (!Array.prototype.remove) {
    Array.prototype.remove = function (item) {
        var index = this.indexOf(item);
        if (index !== -1) {
            return this.splice(index, 1)
        } else {
            if (arguments[1]) {
                throw Error('Array doesn\'t have element')
            } else {
                return undefined
            }
        }
    }
}
if (!Array.range) {
    Array.range = function (num) {
        return Array.apply(null, new Array(num)).map(function(_, i) {return i;})
    }
}


_.mixin({
    deepCopy: function (obj) {
        if (_.isArray(obj)) {
            return obj.map(_.deepCopy);
        } else if (_.isDate(obj)) {
            return new Date(obj);
        } else if (_.isObject(obj)) {
            return _.mapObject(obj, _.deepCopy);
        } else {
            return obj;
        }
    }
});