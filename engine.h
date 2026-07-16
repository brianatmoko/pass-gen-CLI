#ifndef PASSGEN_ENGINE_H
#define PASSGEN_ENGINE_H

#define PASSGEN_SYMBOLS  1
#define PASSGEN_NUMBERS  2
#define PASSGEN_UPPER    4
#define PASSGEN_LOWER    8

#ifdef __cplusplus
extern "C" {
#endif

int generate(char* out, int length, unsigned int flags);

#ifdef __cplusplus
}
#endif

#endif
