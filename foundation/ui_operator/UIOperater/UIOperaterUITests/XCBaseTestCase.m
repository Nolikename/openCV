//
//  XCBaseTestCase.m
//  UIOperaterUITests
//
//  Created by ethanxblin on 2022/5/28.
//

#import "XCBaseTestCase.h"
#import "EPTestConfig.h"

static NSString *systemInterruptionMonitor = @"systemInterruptionMonitor";

@interface XCBaseTestCase()

@property(nonatomic, strong) id systemInterruptionMonitor;

@end

@implementation XCBaseTestCase

- (void)config {
    NSURL *url = [[NSBundle bundleForClass:[self class]] URLForResource:@"config" withExtension:@"json"];
    NSData *data = [[NSData alloc] initWithContentsOfURL:url];
    NSDictionary *dic = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:nil];
    XCTLog(@"初始化配置信息：%@",dic);
    [[EPTestConfig shareConfig] configProductName:dic[@"productName"]];
    [[EPTestConfig shareConfig] configProjectId:dic[@"projectId"]];
}

- (BOOL)setUpWithError:(NSError *__autoreleasing  _Nullable *)error {
    
    [self config];
    
    self.systemInterruptionMonitor = [self addUIInterruptionMonitorWithDescription:systemInterruptionMonitor
                                                                           handler:^BOOL(XCUIElement * _Nonnull interruptingElement) {
        XCTLog(@"接收到中断[%@]，此中断由系统处理！！",interruptingElement.description)
        return NO;
    }];
    return [super setUpWithError:error];
}

- (void)tearDown {
    if (self.systemInterruptionMonitor) {
        [self removeUIInterruptionMonitor:self.systemInterruptionMonitor];
    }
    [super tearDown];
}
@end
