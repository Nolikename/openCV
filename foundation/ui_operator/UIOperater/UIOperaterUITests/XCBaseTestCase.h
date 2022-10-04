//
//  XCBaseTestCase.h
//  UIOperaterUITests
//
//  Created by ethanxblin on 2022/5/28.
//

#import <Foundation/Foundation.h>
#import <XCTest/XCTest.h>

NS_ASSUME_NONNULL_BEGIN
#define XCTLog(fmt,...) \
NSLog((@"[UIOperaterUITests]" fmt), ##__VA_ARGS__);

@interface XCBaseTestCase : XCTestCase

@end

NS_ASSUME_NONNULL_END
