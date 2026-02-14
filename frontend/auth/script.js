// 认证页面脚本

// DOM 加载完成后执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuthPage);
} else {
    initAuthPage();
}

function initAuthPage() {
    // 隐藏页面加载动画
    setTimeout(function() {
        var pageLoader = document.getElementById('page-loader');
        if (pageLoader) {
            pageLoader.classList.add('hidden');
        }
    }, 800);
    
    // 加载预定义姓名列表
    loadPredefinedNames();
    
    // 初始化表单切换
    initFormToggle();
    
    // 初始化密码显示/隐藏
    initPasswordToggle();
    
    // 初始化表单验证
    initFormValidation();
    
    // 初始化表单提交
    initFormSubmit();
}

// 初始化表单切换功能
function initFormToggle() {
    var authTabs = document.querySelectorAll('.auth-tab');
    var formPanels = document.querySelectorAll('.form-panel');
    
    if (authTabs.length > 0 && formPanels.length > 0) {
        authTabs.forEach(function(tab) {
            tab.addEventListener('click', function() {
                switchTab(this);
            });
            
            // 键盘导航支持
            tab.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    switchTab(this);
                } else if (e.key === 'ArrowRight') {
                    e.preventDefault();
                    var nextTab = this.nextElementSibling || authTabs[0];
                    nextTab.focus();
                } else if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    var prevTab = this.previousElementSibling || authTabs[authTabs.length - 1];
                    prevTab.focus();
                }
            });
        });
    }
}

// 切换标签函数
function switchTab(tab) {
    var authTabs = document.querySelectorAll('.auth-tab');
    var formPanels = document.querySelectorAll('.form-panel');
    var targetTab = tab.getAttribute('data-tab');
    
    // 更新标签状态
    authTabs.forEach(function(t) {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
    });
    tab.classList.add('active');
    tab.setAttribute('aria-selected', 'true');
    
    // 更新表单状态
    formPanels.forEach(function(panel) {
        panel.classList.remove('active');
    });
    
    var targetPanel = document.getElementById(targetTab + '-form');
    if (targetPanel) {
        targetPanel.classList.add('active');
        
        // 聚焦到表单的第一个输入框
        var firstInput = targetPanel.querySelector('input[autofocus], input');
        if (firstInput) {
            firstInput.focus();
        }
    }
}

// 初始化密码显示/隐藏功能
function initPasswordToggle() {
    var togglePasswordButtons = document.querySelectorAll('.toggle-password');
    
    if (togglePasswordButtons.length > 0) {
        togglePasswordButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                var passwordInput = this.previousElementSibling;
                var icon = this.querySelector('i');
                
                if (passwordInput && icon) {
                    if (passwordInput.type === 'password') {
                        passwordInput.type = 'text';
                        icon.classList.remove('fa-eye');
                        icon.classList.add('fa-eye-slash');
                        this.setAttribute('aria-pressed', 'true');
                    } else {
                        passwordInput.type = 'password';
                        icon.classList.remove('fa-eye-slash');
                        icon.classList.add('fa-eye');
                        this.setAttribute('aria-pressed', 'false');
                    }
                }
            });
        });
    }
}

// 初始化表单验证功能
function initFormValidation() {
    var forms = document.querySelectorAll('form');
    
    if (forms.length > 0) {
        forms.forEach(function(form) {
            var inputs = form.querySelectorAll('input');
            
            inputs.forEach(function(input) {
                input.addEventListener('input', function() {
                    validateField(this);
                    
                    // 密码强度检测
                    if (input.id === 'register-password') {
                        checkPasswordStrength(input.value);
                    }
                });
                
                input.addEventListener('blur', function() {
                    validateField(this);
                });
            });
        });
    }
}

// 全局变量：存储预定义的姓名列表
var predefinedNames = [];

// 初始化时加载预定义姓名列表
function loadPredefinedNames() {
    fetch('../../data/database/unified_user_data.json')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            if (data && data.names) {
                predefinedNames = data.names;
            }
        })
        .catch(function(error) {
            console.error('加载预定义姓名列表失败:', error);
        });
}

// 验证单个字段
function validateField(input) {
    var errorMessage = input.nextElementSibling;
    var isValid = true;
    var message = '';
    
    if (errorMessage && errorMessage.classList.contains('error-message')) {
        // 验证用户名
        if (input.id === 'login-username' || input.id === 'register-username') {
            if (input.value.trim() === '') {
                message = '用户名不能为空';
                isValid = false;
            } else if (input.value.length < 3) {
                message = '用户名长度至少3位';
                isValid = false;
            } else if (input.value.length > 20) {
                message = '用户名长度不能超过20位';
                isValid = false;
            }
        }
        
        // 验证真实姓名
        if (input.id === 'register-realname') {
            if (input.value.trim() === '') {
                message = '真实姓名不能为空';
                isValid = false;
            } else if (input.value.length < 2) {
                message = '真实姓名长度至少2位';
                isValid = false;
            } else if (input.value.length > 20) {
                message = '真实姓名长度不能超过20位';
                isValid = false;
            } else if (predefinedNames.length > 0 && predefinedNames.indexOf(input.value.trim()) === -1) {
                message = '真实姓名不在预定义列表中';
                isValid = false;
            }
        }
        
        // 验证密码
        if (input.id === 'login-password' || input.id === 'register-password') {
            if (input.value === '') {
                message = '密码不能为空';
                isValid = false;
            } else if (input.id === 'register-password' && input.value.length < 8) {
                message = '密码长度至少8位';
                isValid = false;
            }
        }
        
        // 验证确认密码
        if (input.id === 'register-confirm-password') {
            var passwordInput = document.getElementById('register-password');
            if (passwordInput) {
                if (input.value === '') {
                    message = '请确认密码';
                    isValid = false;
                } else if (input.value !== passwordInput.value) {
                    message = '两次输入的密码不一致';
                    isValid = false;
                }
            }
        }
        
        // 显示错误信息
        errorMessage.textContent = message;
        if (isValid) {
            errorMessage.style.display = 'none';
            errorMessage.classList.remove('show');
        } else {
            errorMessage.style.display = 'block';
            // 触发重排，确保动画正常播放
            errorMessage.offsetHeight;
            errorMessage.classList.add('show');
        }
        
        // 设置输入框样式 - 与Bulma兼容
        if (input.classList.contains('input')) {
            if (!isValid) {
                input.classList.add('is-danger');
                // 添加Bulma的错误状态样式
                var control = input.parentElement;
                if (control && control.classList.contains('control')) {
                    control.classList.add('has-icons-right');
                }
            } else {
                input.classList.remove('is-danger');
                // 移除Bulma的错误状态样式
                var control = input.parentElement;
                if (control && control.classList.contains('control')) {
                    control.classList.remove('has-icons-right');
                }
            }
        }
    }
    
    return isValid;
}

// 验证整个表单
function validateForm(form) {
    var inputs = form.querySelectorAll('input[required]');
    var isValid = true;
    
    inputs.forEach(function(input) {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// 初始化表单提交
function initFormSubmit() {
    var loginForm = document.getElementById('login-form');
    var registerForm = document.getElementById('register-form');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleLoginSubmit(this);
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleRegisterSubmit(this);
        });
    }
}

// 处理登录表单提交
function handleLoginSubmit(form) {
    if (validateForm(form)) {
        // 获取登录按钮
        var loginButton = form.querySelector('.button.is-primary');
        
        // 显示加载状态
        showLoading();
        
        // 为按钮添加加载状态
        if (loginButton) {
            loginButton.classList.add('is-loading');
            loginButton.disabled = true;
        }
        
        // 获取表单数据
        var username = document.getElementById('login-username').value;
        var password = document.getElementById('login-password').value;
        
        // 构建form-data
        var formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        
        // 调用后端API
        fetch('/api/auth/login', {
            method: 'POST',
            body: formData
        })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // 隐藏加载状态
            hideLoading();
            
            // 移除按钮加载状态
            if (loginButton) {
                loginButton.classList.remove('is-loading');
                loginButton.disabled = false;
            }
            
            if (data.code === 200) {
                // 登录成功
                console.log('登录成功:', data);
                
                // 设置token和用户信息到localStorage
                localStorage.setItem('token', data.data.access_token);
                localStorage.setItem('user', JSON.stringify(data.data.user));
                
                // 显示成功消息
                showNotification('登录成功', 'success');
                
                // 跳转到桌面页面
                setTimeout(function() {
                    window.location.href = '../desktop/index.html';
                }, 1000);
            } else {
                // 登录失败
                console.error('登录失败:', data);
                // 处理不同的错误格式
                var errorMessage = '登录失败';
                if (data.message) {
                    errorMessage = data.message;
                } else if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        // 处理detail是对象数组的情况
                        var errorMessages = [];
                        for (var i = 0; i < data.detail.length; i++) {
                            var item = data.detail[i];
                            if (item.msg) {
                                errorMessages.push(item.msg);
                            } else if (typeof item === 'string') {
                                errorMessages.push(item);
                            }
                        }
                        errorMessage = errorMessages.join('; ');
                    } else if (typeof data.detail === 'object') {
                        // 处理detail是对象的情况
                        errorMessage = JSON.stringify(data.detail);
                    } else {
                        // 处理detail是字符串的情况
                        errorMessage = data.detail;
                    }
                }
                showNotification(errorMessage, 'error');
            }
        })
        .catch(function(error) {
            // 隐藏加载状态
            hideLoading();
            
            // 移除按钮加载状态
            if (loginButton) {
                loginButton.classList.remove('is-loading');
                loginButton.disabled = false;
            }
            
            console.error('登录请求错误:', error);
            showNotification('登录请求失败，请检查网络连接', 'error');
        });
    }
}

// 处理注册表单提交
function handleRegisterSubmit(form) {
    if (validateForm(form)) {
        // 获取注册按钮
        var registerButton = form.querySelector('.button.is-primary');
        
        // 显示加载状态
        showLoading();
        
        // 为按钮添加加载状态
        if (registerButton) {
            registerButton.classList.add('is-loading');
            registerButton.disabled = true;
        }
        
        // 获取表单数据
        var username = document.getElementById('register-username').value;
        var realname = document.getElementById('register-realname').value;
        var password = document.getElementById('register-password').value;
        
        // 构建请求体
        var requestData = {
            username: username,
            realname: realname,
            password: password,
            email: null
        };
        
        // 打印请求数据到控制台
        console.log('注册请求数据:', requestData);
        console.log('预定义姓名列表:', predefinedNames);
        console.log('真实姓名是否在预定义列表中:', predefinedNames.indexOf(realname) !== -1);
        
        // 调用后端API
        fetch('/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            // 检查响应状态
            if (!response.ok) {
                // 尝试获取响应文本
                return response.text().then(function(text) {
                    // 抛出错误，包含响应文本
                    throw new Error(text || '请求失败');
                });
            }
            // 尝试解析JSON响应
            return response.json().catch(function() {
                // 如果解析失败，抛出错误
                throw new Error('无效的响应格式');
            });
        })
        .then(function(data) {
            // 隐藏加载状态
            hideLoading();
            
            // 移除按钮加载状态
            if (registerButton) {
                registerButton.classList.remove('is-loading');
                registerButton.disabled = false;
            }
            
            if (data.code === 200) {
                // 注册成功
                console.log('注册成功:', data);
                
                // 显示成功消息
                showNotification('注册成功，请登录', 'success');
                
                // 切换到登录表单
                var loginTab = document.querySelector('.auth-tab[data-tab="login"]');
                if (loginTab) {
                    loginTab.click();
                }
            } else {
                // 注册失败
                console.error('注册失败:', data);
                // 处理不同的错误格式
                var errorMessage = '注册失败';
                if (data.message) {
                    errorMessage = data.message;
                } else if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        // 处理detail是对象数组的情况
                        var errorMessages = [];
                        for (var i = 0; i < data.detail.length; i++) {
                            var item = data.detail[i];
                            if (item.msg) {
                                errorMessages.push(item.msg);
                            } else if (typeof item === 'string') {
                                errorMessages.push(item);
                            }
                        }
                        errorMessage = errorMessages.join('; ');
                    } else if (typeof data.detail === 'object') {
                        // 处理detail是对象的情况
                        errorMessage = JSON.stringify(data.detail);
                    } else {
                        // 处理detail是字符串的情况
                        errorMessage = data.detail;
                    }
                }
                showNotification(errorMessage, 'error');
            }
        })
        .catch(function(error) {
            // 隐藏加载状态
            hideLoading();
            
            // 移除按钮加载状态
            if (registerButton) {
                registerButton.classList.remove('is-loading');
                registerButton.disabled = false;
            }
            
            console.error('注册请求错误:', error);
            // 提取错误信息
            var errorMessage = error.message || '注册请求失败，请检查网络连接';
            // 处理可能的内部服务器错误信息
            if (errorMessage.startsWith('Internal Server Error')) {
                errorMessage = '服务器内部错误，请稍后再试';
            }
            showNotification(errorMessage, 'error');
        });
    }
}

// 显示加载状态
function showLoading() {
    var loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.add('active');
    }
}

// 隐藏加载状态
function hideLoading() {
    var loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('active');
    }
}

// 显示通知
function showNotification(message, type) {
    // 创建通知元素
    var notification = document.createElement('div');
    notification.className = 'notification ' + type;
    notification.textContent = message;
    
    // 设置通知样式
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '15px 20px';
    notification.style.borderRadius = '8px';
    notification.style.zIndex = '9999';
    notification.style.opacity = '0';
    notification.style.transform = 'translateX(100%)';
    notification.style.transition = 'all 0.3s ease';
    
    // 设置不同类型的通知样式
    if (type === 'success') {
        notification.style.backgroundColor = '#10B981';
        notification.style.color = '#FFFFFF';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#EF4444';
        notification.style.color = '#FFFFFF';
    } else {
        notification.style.backgroundColor = '#3B82F6';
        notification.style.color = '#FFFFFF';
    }
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(function() {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // 自动隐藏
    setTimeout(function() {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        
        // 移除元素
        setTimeout(function() {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// 工具函数：获取元素
function getElementById(id) {
    return document.getElementById(id);
}

// 工具函数：添加事件监听器
function addEventListener(element, event, callback) {
    if (element && element.addEventListener) {
        element.addEventListener(event, callback);
    } else if (element && element.attachEvent) {
        // 兼容旧IE
        element.attachEvent('on' + event, callback);
    }
}

// 工具函数：检查元素是否包含类
function hasClass(element, className) {
    if (element.classList) {
        return element.classList.contains(className);
    } else {
        // 兼容旧IE
        return new RegExp('\\b' + className + '\\b').test(element.className);
    }
}

// 工具函数：添加类
function addClass(element, className) {
    if (element.classList) {
        element.classList.add(className);
    } else {
        // 兼容旧IE
        if (!hasClass(element, className)) {
            element.className += ' ' + className;
        }
    }
}

// 工具函数：移除类
function removeClass(element, className) {
    if (element.classList) {
        element.classList.remove(className);
    } else {
        // 兼容旧IE
        element.className = element.className.replace(new RegExp('\\b' + className + '\\b', 'g'), '').trim();
    }
}

// 密码强度检测函数
function checkPasswordStrength(password) {
    var strength = 0;
    var strengthText = '弱';
    var strengthClass = 'weak';
    
    // 长度检查
    if (password.length >= 8) {
        strength += 1;
    }
    if (password.length >= 12) {
        strength += 1;
    }
    
    // 复杂度检查
    if (/[A-Z]/.test(password)) {
        strength += 1;
    }
    if (/[0-9]/.test(password)) {
        strength += 1;
    }
    if (/[^A-Za-z0-9]/.test(password)) {
        strength += 1;
    }
    
    // 确定强度级别
    if (strength >= 4) {
        strengthText = '强';
        strengthClass = 'strong';
    } else if (strength >= 2) {
        strengthText = '中';
        strengthClass = 'medium';
    }
    
    // 更新强度指示器
    var strengthBars = document.querySelectorAll('.password-strength-bar');
    var strengthTextElement = document.getElementById('password-strength-text');
    
    if (strengthBars.length > 0 && strengthTextElement) {
        strengthBars.forEach(function(bar, index) {
            // 移除所有强度类
            removeClass(bar, 'weak');
            removeClass(bar, 'medium');
            removeClass(bar, 'strong');
            
            // 根据强度添加相应的类
            if (index < Math.min(strength, strengthBars.length)) {
                addClass(bar, strengthClass);
            }
        });
        
        // 更新强度文本
        strengthTextElement.textContent = strengthText;
        
        // 移除所有强度类
        removeClass(strengthTextElement, 'weak');
        removeClass(strengthTextElement, 'medium');
        removeClass(strengthTextElement, 'strong');
        
        // 添加当前强度类
        addClass(strengthTextElement, strengthClass);
    }
}
