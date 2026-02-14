// 设置页面脚本

// DOM 加载完成后执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSettingsPage);
} else {
    initSettingsPage();
}

function initSettingsPage() {
    // 初始化页面导航
    initPageNavigation();
    
    // 初始化密码显示/隐藏
    initPasswordToggle();
    
    // 初始化表单验证
    initFormValidation();
    
    // 初始化表单提交
    initFormSubmit();
    
    // 初始化退出登录
    initLogout();
    
    // 加载用户信息
    loadUserInfo();
}

// 初始化页面导航
function initPageNavigation() {
    var navLinks = document.querySelectorAll('.nav-link');
    var contentPages = document.querySelectorAll('.content-page');
    
    if (navLinks.length > 0) {
        navLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                var targetPage = this.getAttribute('data-page');
                
                // 更新导航链接状态
                navLinks.forEach(function(navLink) {
                    navLink.classList.remove('active');
                });
                this.classList.add('active');
                
                // 显示对应页面
                contentPages.forEach(function(page) {
                    page.style.display = 'none';
                });
                
                var targetPageElement = document.getElementById(targetPage + '-page');
                if (targetPageElement) {
                    targetPageElement.style.display = 'block';
                }
            });
        });
    }
}

// 初始化密码显示/隐藏
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

// 初始化表单验证
function initFormValidation() {
    var forms = document.querySelectorAll('form');
    
    if (forms.length > 0) {
        forms.forEach(function(form) {
            var inputs = form.querySelectorAll('input, textarea');
            
            inputs.forEach(function(input) {
                input.addEventListener('input', function() {
                    validateField(this);
                    
                    // 密码强度检测
                    if (input.id === 'new-password') {
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

// 验证单个字段
function validateField(input) {
    var errorMessage = input.nextElementSibling;
    var isValid = true;
    var message = '';
    
    if (errorMessage && errorMessage.classList.contains('error-message')) {
        // 验证用户名
        if (input.id === 'username') {
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
        
        // 验证手机号
        if (input.id === 'phone') {
            if (input.value.trim() !== '' && !/^1[3-9]\d{9}$/.test(input.value)) {
                message = '手机号格式不正确';
                isValid = false;
            }
        }
        
        // 验证QQ号
        if (input.id === 'qq') {
            if (input.value.trim() !== '' && !/^[1-9]\d{4,10}$/.test(input.value)) {
                message = 'QQ号格式不正确';
                isValid = false;
            }
        }
        
        // 验证微信号
        if (input.id === 'wechat') {
            if (input.value.trim() !== '' && !/^[a-zA-Z0-9_-]{6,20}$/.test(input.value)) {
                message = '微信号格式不正确（6-20位字母、数字、下划线或连字符）';
                isValid = false;
            }
        }
        
        // 验证住址
        if (input.id === 'address') {
            if (input.value.trim() !== '' && input.value.length > 100) {
                message = '住址长度不能超过100位';
                isValid = false;
            }
        }
        
        // 验证个人签名
        if (input.id === 'bio') {
            if (input.value.trim() !== '' && input.value.length > 200) {
                message = '个人签名长度不能超过200位';
                isValid = false;
            }
        }
        
        // 验证生日
        if (input.id === 'birthday') {
            if (input.value.trim() !== '' && !/^\d{4}-\d{2}-\d{2}$/.test(input.value)) {
                message = '生日格式不正确，应为 YYYY-MM-DD';
                isValid = false;
            }
        }
        
        // 验证原密码
        if (input.id === 'current-password') {
            if (input.value === '') {
                message = '原密码不能为空';
                isValid = false;
            }
        }
        
        // 验证新密码
        if (input.id === 'new-password') {
            if (input.value === '') {
                message = '新密码不能为空';
                isValid = false;
            } else if (input.value.length < 8) {
                message = '新密码长度至少8位';
                isValid = false;
            }
        }
        
        // 验证确认密码
        if (input.id === 'confirm-password') {
            var newPasswordInput = document.getElementById('new-password');
            if (newPasswordInput) {
                if (input.value === '') {
                    message = '请确认新密码';
                    isValid = false;
                } else if (input.value !== newPasswordInput.value) {
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
        if (input.classList.contains('input') || input.classList.contains('textarea')) {
            if (!isValid) {
                input.classList.add('is-danger');
            } else {
                input.classList.remove('is-danger');
            }
        }
    }
    
    return isValid;
}

// 验证整个表单
function validateForm(form) {
    var inputs = form.querySelectorAll('input[required], textarea[required]');
    var isValid = true;
    
    inputs.forEach(function(input) {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// 密码强度检测
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
            bar.classList.remove('weak', 'medium', 'strong');
            
            // 根据强度添加相应的类
            if (index < Math.min(strength, strengthBars.length)) {
                bar.classList.add(strengthClass);
            }
        });
        
        // 更新强度文本
        strengthTextElement.textContent = strengthText;
        
        // 移除所有强度类
        strengthTextElement.classList.remove('weak', 'medium', 'strong');
        
        // 添加当前强度类
        strengthTextElement.classList.add(strengthClass);
    }
}

// 初始化表单提交
function initFormSubmit() {
    var profileForm = document.getElementById('profile-form');
    var passwordForm = document.getElementById('password-form');
    
    if (profileForm) {
        profileForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handleProfileSubmit(this);
        });
        
        // 取消按钮
        var cancelProfileButton = document.getElementById('cancel-profile');
        if (cancelProfileButton) {
            cancelProfileButton.addEventListener('click', function() {
                loadUserInfo();
            });
        }
    }
    
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            handlePasswordSubmit(this);
        });
        
        // 取消按钮
        var cancelPasswordButton = document.getElementById('cancel-password');
        if (cancelPasswordButton) {
            cancelPasswordButton.addEventListener('click', function() {
                passwordForm.reset();
                var errorMessages = passwordForm.querySelectorAll('.error-message');
                errorMessages.forEach(function(message) {
                    message.style.display = 'none';
                    message.classList.remove('show');
                });
                var passwordInputs = passwordForm.querySelectorAll('input');
                passwordInputs.forEach(function(input) {
                    input.classList.remove('is-danger');
                });
            });
        }
    }
}

// 处理个人资料表单提交
function handleProfileSubmit(form) {
    if (validateForm(form)) {
        // 显示加载状态
        showLoading();
        
        // 获取表单数据
        var username = document.getElementById('username').value;
        var phone = document.getElementById('phone').value;
        var qq = document.getElementById('qq').value;
        var wechat = document.getElementById('wechat').value;
        var address = document.getElementById('address').value;
        var bio = document.getElementById('bio').value;
        var birthday = document.getElementById('birthday').value;
        
        // 构建请求体
        var requestData = {
            username: username,
            phone: phone,
            qq: qq,
            wechat: wechat,
            address: address,
            bio: bio,
            birthday: birthday
        };
        
        // 获取token
        var token = localStorage.getItem('token');
        if (!token) {
            hideLoading();
            showNotification('请先登录', 'error');
            window.location.href = '../auth/index.html';
            return;
        }
        
        // 调用后端API
        fetch('/api/user/profile', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            if (!response.ok) {
                return response.json().then(function(data) {
                    throw new Error(data.detail || '更新失败');
                }).catch(function() {
                    throw new Error('更新失败');
                });
            }
            return response.json();
        })
        .then(function(data) {
            hideLoading();
            if (data.code === 200) {
                showNotification('个人资料更新成功', 'success');
            } else {
                showNotification(data.message || '更新失败', 'error');
            }
        })
        .catch(function(error) {
            hideLoading();
            showNotification(error.message || '更新失败', 'error');
        });
    }
}

// 处理密码修改表单提交
function handlePasswordSubmit(form) {
    if (validateForm(form)) {
        // 显示加载状态
        showLoading();
        
        // 获取表单数据
        var currentPassword = document.getElementById('current-password').value;
        var newPassword = document.getElementById('new-password').value;
        
        // 构建请求体
        var requestData = {
            current_password: currentPassword,
            new_password: newPassword
        };
        
        // 获取token
        var token = localStorage.getItem('token');
        if (!token) {
            hideLoading();
            showNotification('请先登录', 'error');
            window.location.href = '../auth/index.html';
            return;
        }
        
        // 调用后端API
        fetch('/api/user/password', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(requestData)
        })
        .then(function(response) {
            if (!response.ok) {
                return response.json().then(function(data) {
                    throw new Error(data.detail || '密码修改失败');
                }).catch(function() {
                    throw new Error('密码修改失败');
                });
            }
            return response.json();
        })
        .then(function(data) {
            hideLoading();
            if (data.code === 200) {
                showNotification('密码修改成功', 'success');
                form.reset();
            } else {
                showNotification(data.message || '密码修改失败', 'error');
            }
        })
        .catch(function(error) {
            hideLoading();
            showNotification(error.message || '密码修改失败', 'error');
        });
    }
}

// 初始化退出登录
function initLogout() {
    var confirmLogoutButton = document.getElementById('confirm-logout');
    var cancelLogoutButton = document.getElementById('cancel-logout');
    
    if (confirmLogoutButton) {
        confirmLogoutButton.addEventListener('click', function() {
            // 显示加载状态
            showLoading();
            
            // 模拟API请求
            setTimeout(function() {
                hideLoading();
                // 清除本地存储
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                // 跳转到登录页
                window.location.href = '../auth/index.html';
            }, 1000);
        });
    }
    
    if (cancelLogoutButton) {
        cancelLogoutButton.addEventListener('click', function() {
            // 切换到个人资料页面
            var profileLink = document.querySelector('.nav-link[data-page="profile"]');
            if (profileLink) {
                profileLink.click();
            }
        });
    }
}

// 加载用户信息
function loadUserInfo() {
    // 显示加载状态
    showLoading();
    
    // 获取token
    var token = localStorage.getItem('token');
    if (!token) {
        hideLoading();
        showNotification('请先登录', 'error');
        window.location.href = '../auth/index.html';
        return;
    }
    
    // 调用后端API
    fetch('/api/user/profile', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
    .then(function(response) {
        if (!response.ok) {
            return response.json().then(function(data) {
                throw new Error(data.detail || '获取用户信息失败');
            }).catch(function() {
                throw new Error('获取用户信息失败');
            });
        }
        return response.json();
    })
    .then(function(data) {
        hideLoading();
        if (data.code === 200) {
                var userData = data.data;
                // 填充表单数据
                document.getElementById('user-id').value = userData.user_id;
                document.getElementById('real-name').value = userData.realname;
                document.getElementById('username').value = userData.username;
                document.getElementById('phone').value = userData.phone || '';
                document.getElementById('qq').value = userData.qq || '';
                document.getElementById('wechat').value = userData.wechat || '';
                document.getElementById('address').value = userData.address || '';
                document.getElementById('bio').value = userData.bio || '';
                document.getElementById('birthday').value = userData.birthday || '';
            } else {
                showNotification(data.message || '获取用户信息失败', 'error');
            }
    })
    .catch(function(error) {
        hideLoading();
        showNotification(error.message || '获取用户信息失败', 'error');
    });
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
    
    // 添加到页面
    document.body.appendChild(notification);
    
    // 显示动画
    setTimeout(function() {
        notification.classList.add('show');
    }, 10);
    
    // 自动隐藏
    setTimeout(function() {
        notification.classList.remove('show');
        setTimeout(function() {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}
