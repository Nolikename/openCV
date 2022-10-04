//
//  DMDataManager.m
//  Liuliang
//
//  Created by ihenryhuang(黄洪) on 2020/4/8.
//  Copyright © 2020 Tencent. All rights reserved.
//

#import "DMDataManager.h"
#import "NetSpeed.h"

@interface DMDataManager()

@end

@implementation DMDataManager

+ (DMDataManager *)defaultDB {
    static DMDataManager *manager;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        manager=[[DMDataManager alloc] init];
        
    });
    return manager;
}

- (void)addNetworkTrafficLog:(DMNetworkTrafficLog *)log{
    
    if ([log.type isEqualToString:@"DMNetworkTrafficDataTypeRequest"]) {
        self.totalSend += log.length;
    }else{
        self.totalRev += log.length;
    }
    
}

@end
