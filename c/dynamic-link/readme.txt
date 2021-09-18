关于-fPIC, -fpic, -pie的参数可以在../pie-pic/readme.txt看补充资料;

这里3个demo分别用不同参数编译, 用于展示可执行文件中符号, 动态链接库符号在不同参数下的加载地址

## 可执行文件符号加载地址
对于main以及main_pic来说, main函数的加载地址是一样;
对于main_pie来说, 由于链接的时候指定了-pie参数, main的加载地址也是随机的;

## 动态链接库符号加载地址
对于main来说, 由于main.c没有使用-fPIC进行编译,所以hello, world的符号地址也是一样的;
对于main_pic以及main_pie来说, 由于main.c 使用了-fPIC进行编译, hello, world 地址是随机加载的;
