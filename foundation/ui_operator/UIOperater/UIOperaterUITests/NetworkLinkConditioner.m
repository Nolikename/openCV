//
//  NetworkLinkConditioner.m
//  UIOperateUITests
//
//  Created by huang on 2021/1/31.
//  Copyright (c) 2020年 Tencent. All rights reserved.
//

#import <XCTest/XCTest.h>

#define DELETE_OLD_CONFIG YES

/// 弱网配置
@interface NetworkLinkConditioner : XCTestCase

/// 偏好设置App
@property(nonatomic)XCUIApplication *preference;

/// 设置
@property(nonatomic, copy)NSDictionary *config;

@end

/// 弱网配置
@implementation NetworkLinkConditioner

- (void)setUp {
    self.config = @{
        @"bus":@{
                @"name":@"bus",
                @"In Brandwidth":@"360",
                @"In Packet Loss":@"2",
                @"In Delay":@"111",
                @"Out Brandwidth":@"20",
                @"Out Packet Loss":@"2",
                @"Out Delay":@"111",
                @"DNS Delay":@"0"
        },
        @"railway":@{
                @"name":@"railway",
                @"In Brandwidth":@"864",
                @"In Packet Loss":@"5",
                @"In Delay":@"121",
                @"Out Brandwidth":@"48",
                @"Out Packet Loss":@"5",
                @"Out Delay":@"121",
                @"DNS Delay":@"0"
        },
        @"subway":@{
                @"name":@"subway",
                @"In Brandwidth":@"864",
                @"In Packet Loss":@"2",
                @"In Delay":@"121",
                @"Out Brandwidth":@"48",
                @"Out Packet Loss":@"2",
                @"Out Delay":@"121",
                @"DNS Delay":@"0"
        }
    };
}

/// 巴士
-(void)testBus{
    [self config:@"bus"];
}

/// 高铁
-(void)testRailway{
    [self config:@"railway"];
}

/// 地铁
-(void)testSubway{
    [self config:@"subway"];
}


/// 每次测试结束后停止弱网络配置
-(void)testDisable{

    [self enterConfigPage];
    [self disable];
    [self.preference terminate];
    
}

#pragma Private Func

/// 禁用
-(void)disable{
    if ([self isNetConfigSwitchOn]) {
        [[self.preference.switches elementBoundByIndex:0] tap];
    }
}

/// 启用
-(void)enable{
    if (![self isNetConfigSwitchOn]) {
        [[self.preference.switches elementBoundByIndex:0] tap];
    }
}

/// 判断开关是否打开
-(BOOL)isNetConfigSwitchOn{
    NSString *value = [self.preference.switches elementBoundByIndex:0].value;
    if ([value isEqualToString:@"0"]) {
        return NO;
    }else{
        return YES;
    }
}

/// 打开偏好设置
-(void)enterConfigPage{
    
    [self.preference terminate];
    
    [self.preference activate];

    sleep(2);
    XCUIElement *developerInChinese =  self.preference.tables.staticTexts[@"开发者"];
    [developerInChinese tap];

    sleep(2);
    [self.preference.tables.staticTexts[@"Network Link Conditioner"] tap];
    
}

#pragma getter 偏好设置
- (XCUIApplication *)preference{
    if (!_preference) {
        _preference = [[XCUIApplication alloc] initWithBundleIdentifier:@"com.apple.Preferences"];
    }
    return _preference;
}

-(void)config:(NSString *)name{
    
    [self enterConfigPage];
    
    if (![self isAlreadyConfiged:name]) {
        XCUIElement *addProfile = self.preference.tables.staticTexts[@"Add a profile…"];
        [addProfile tap];
        
        // 输入配置名称
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"Name"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"name"]];
        }
        
        // 下行带宽
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"In Bandwidth"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"In Brandwidth"]];
             
        }
        // 下行丢包率
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"In Packet Loss"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"In Packet Loss"]];
             
        }

        // 下行延迟
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"In Delay"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"In Delay"]];
        }
        
        // 上行带宽
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"Out Bandwidth"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"Out Bandwidth"]];
             
        }
        
        // 上行丢包率
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"Out Packet Loss"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"Out Packet Loss"]];
             
        }
        
        // 上行延迟
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"Out Delay"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"Out Delay"]];
        }
        
        // DNS延迟
        {
            XCUIElement *usernameTextField = self.preference.textFields[@"DNS Delay"];
            [usernameTextField tap];
            [usernameTextField typeText:self.config[name][@"DNS Delay"]];
             
        }
        
        // Interface
        {
            XCUIElement *usernameTextField = self.preference.tables.staticTexts[@"Interface"];
            [usernameTextField tap];
        }
        
        // Interface
        {
            XCUIElement *usernameTextField = self.preference.tables.staticTexts[@"Cellular"];
            [usernameTextField tap];
        }
        [self.preference.navigationBars[@"Interface"].buttons[@"Add a profile…"] tap];
        // 存储
        [self.preference.navigationBars[@"Add a profile…"].buttons[@"存储"] tap];

    }

    [self.preference.tables.cells[name].staticTexts[@"Custom"] tap];
    sleep(3);
    [self enable];
}

// 判断是否已经
-(BOOL)isAlreadyConfiged:(NSString *)name{
    
    XCUIElement *elment = self.preference.tables.cells[name].staticTexts[@"Custom"];
    
    if ([elment exists]) {
        return  YES;
    }else{
        return  NO;
    }
}

@end
