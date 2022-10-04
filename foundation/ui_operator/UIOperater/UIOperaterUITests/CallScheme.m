//
//  CallScheme.m
//  UIOperaterUITests
//
//  Created by henry on 2021/3/24.
//

#import <XCTest/XCTest.h>

@interface CallScheme : XCTestCase

@end

@implementation CallScheme

-(void)testCallScheme{
    
    for (int i = 0; i < 4; i++) {
        
        XCUIApplication *safari = [[XCUIApplication alloc] initWithBundleIdentifier:@"com.apple.mobilesafari"];
        [safari terminate];
        [safari launch];
        XCUIElement *inputTf = safari.otherElements[@"URL"];
        XCTAssertTrue([inputTf waitForExistenceWithTimeout:3]);
        [inputTf tap];
        [safari.textFields[@"URL"] typeText:@"weishi://performancetestfeed?feed_id=6VNwTLi471G0Q00IS"];
        [safari.buttons[@"前往"] tap];
        [safari.buttons[@"打开"] tap];
        sleep(10);
        XCUIApplication *microvision = [[XCUIApplication alloc] initWithBundleIdentifier:@"com.tencent.microvision.dailybuild"];
        [microvision terminate];
        
    }
}

@end

