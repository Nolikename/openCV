//
//  Launch.m
//  UIOperaterUITests
//
//  Created by henry on 2021/2/1.
//  Copyright (c) 2020年 Tencent. All rights reserved.
//

#import <XCTest/XCTest.h>
#import "XCBaseTestCase.h"
#import "PerfDogTrackerFactory.h"
#import "PerfDogConst.h"

static NSString* launchInterruptionMonitor = @"launchInterruptionMonitor";

/// 启动测试
@interface Launch : XCBaseTestCase
@property(nonatomic, strong) id launchInterruptionMonitor;
@end

/// 启动测试
@implementation Launch

/// 处理弹框: “软件许可协议和隐藏政策弹窗”
- (void)dismissProxyAlertView:(XCUIApplication *)app {

    XCUIElement *content = app.scrollViews.otherElements.firstMatch;
    XCUIElement *title = content.firstMatch.staticTexts.firstMatch;
    if (![title.label containsString:@"软件许可协议和隐私政策"]) {
        return;
    }

    XCTLog(@"找到“软件许可协议和隐私政策”弹框");

    if (app.scrollViews.otherElements.count <= 1) {
        XCTAssert(nil,@"元素数量不符合预期，请检查app（软件许可协议和隐私政策）的弹窗界面是否更新了。");
        return;
    }

    XCUIElement *actions = [app.scrollViews.otherElements elementBoundByIndex:1];
    XCUIElement *button = actions.buttons.firstMatch;
    XCTAssert([button waitForExistenceWithTimeout:10], @"没找到'同意并继续'按钮，请检查app");
    // tap
    [button tap];
    XCTLog(@"完成处理弹框: “软件许可协议和隐藏政策弹窗”");
}

/// 处理自定义“开启权限，享受完整体验” 浮块
- (void)dismissPemissionFloatPanel:(XCUIApplication *)app {
    if (app.scrollViews.otherElements.count <= 2) {
        return;
    }
    XCUIElement *panel = app.scrollViews.firstMatch;

    XCUIElement *allowNotify = [panel.otherElements elementBoundByIndex:1];
    XCUIElement *staticText = allowNotify.staticTexts[@"允许推送通知"];
    if (![staticText waitForExistenceWithTimeout:10]) {
        return;
    }

    XCTLog(@"找到自定义“开启权限，享受完整体验” 浮块");

    XCUIElement *okBtn = [panel.otherElements elementBoundByIndex:2];
    XCTAssert([okBtn waitForExistenceWithTimeout:10], @"不符合预期，在“开启权限，享受完整体验的浮块上没发现按钮”");
    [okBtn tap];
    XCTLog(@"完成处理自定义“开启权限，享受完整体验” 浮块");
}

- (void)setUp {
    [super setUp];
    self.continueAfterFailure = NO;

    self.launchInterruptionMonitor = [self addUIInterruptionMonitorWithDescription:launchInterruptionMonitor
                                                                           handler:^BOOL(XCUIElement * _Nonnull interruptingElement) {
        XCUIElement *allowButton = interruptingElement.buttons[@"使用App时允许"];
        if (allowButton.exists) {
            [allowButton tap];
            XCTLog(@"接收到中断[%@]，中断被Launch处理了！！",interruptingElement.description)
            return YES;
        }
        XCTLog(@"接收到中断[%@]，此中断Launch不处理！！",interruptingElement.description)
        return NO;
    }];
}
- (void)tearDown {
    if (self.launchInterruptionMonitor) {
        [self removeUIInterruptionMonitor:self.launchInterruptionMonitor];
    }
    [super tearDown];
}

- (void)testOpenSafari {
    XCUIApplication *safari = [[XCUIApplication alloc] initWithBundleIdentifier:@"com.apple.mobilesafari"];
    XCTLog(@"Safari[%p]状态 %@", safari, @(safari.state));
    [safari terminate];
    [safari launch];
}

- (void)testFirstLaunch {

    NSDictionary *env = [[NSProcessInfo processInfo] environment];
    NSString *bundleId = [env objectForKey:@"testAppBundleId"];
    XCTAssert(bundleId.length > 0, @"初始传入的bundle id为空，请检查！！！");
    XCTLog(@"准备启动App %@", bundleId);
    XCUIApplication *app = [[XCUIApplication alloc] initWithBundleIdentifier:bundleId];
    XCTLog(@"App[%p]状态 %@", app, @(app.state));

    [app launch];

    // 处理弹框
    [self dismissProxyAlertView:app];
    // 处理浮块
    [self dismissPemissionFloatPanel:app];

    // 以发现“首页” 并可点击，做为成功标志。
    XCUIElement *homeBtn = app.buttons[@"首页"];
    XCTAssert([homeBtn waitForExistenceWithTimeout:30],@"没有找到“首页”按扭，不符合预期");
    [homeBtn tap];
}

- (void)testPerfdog {
    /*CaseAdditionInfo start
     {
     "FT=基础FT",
     "模块=基础应用",
     "功能=性能测试",
     "测试分类=性能",
     "测试阶段=全用例",
     "管理者=jacknli",
     "创建者=jacknli",
     "用例等级=P00",
     "用例类型=1",
     "被测函数=",
     "用例描述=测试"
     }
     CaseAdditionInfo end*/
    NSDictionary *env = [[NSProcessInfo processInfo] environment];
    NSString *bundleId = [env objectForKey:@"testAppBundleId"];
    XCTAssert(bundleId.length > 0, @"初始传入的bundle id为空，请检查！！！");
    XCTLog(@"准备启动App %@", bundleId);
    XCUIApplication *app = [[XCUIApplication alloc] initWithBundleIdentifier:bundleId];
    XCTLog(@"App[%p]状态 %@", app, @(app.state));

    [app launch];

    // 处理弹框
    [self dismissProxyAlertView:app];
    // 处理浮块
    [self dismissPemissionFloatPanel:app];


    NSMutableDictionary *cpuMeasure = [@{} mutableCopy];
    cpuMeasure[@"index"] = PerfDogIndexAppUsage;
    cpuMeasure[@"name"] = @"cpu";
    cpuMeasure[@"threshold"] = @(100);
    cpuMeasure[@"unit"] = @"%";
    cpuMeasure[@"calculationMethod"] = CalculationMethodDiff;
    cpuMeasure[@"calculationStage"] = @"1,2";
    cpuMeasure[@"computingPercent"] = @(90);

    Tracker *tracker = [[PerfDogTrackerFactory alloc] createTrackerWithCaseName:@"测试Perfdog用例" indexList:@[cpuMeasure]];
    [tracker startTrace];

    // 第一段需要采集
    [tracker addStageToIndicator:@"1" index:@""];
    sleep(20);//稳定后采集3秒获取平均值
    [tracker addEndTimeToStage:@"" stageIndex:@"1" index:@""];

    [tracker addStageToIndicator:@"2" index:@""];
    sleep(20);//稳定后采集3秒获取平均值
    [tracker addEndTimeToStage:@"" stageIndex:@"2" index:@""];
    // 结束追踪
    [tracker stopTrace];

    [app terminate];
}

@end
