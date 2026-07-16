#include "engine.h"
#include <cstring>
#include <fstream>
#include <vector>

static const char SYM[]  = "!@#$%^&*()-_=+[]{}|;:,.<>?";
static const char NUM[]  = "0123456789";
static const char UPP[]  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
static const char LOW[]  = "abcdefghijklmnopqrstuvwxyz";

static bool get_rand(unsigned char* buf, int count) {
    std::ifstream urandom("/dev/urandom", std::ios::binary);
    if (!urandom) return false;
    urandom.read(reinterpret_cast<char*>(buf), count);
    return urandom.gcount() == count;
}

extern "C" int generate(char* out, int length, unsigned int flags) {
    if (length < 1 || length > 4096) return -1;

    const char* pools[4];
    int pool_sizes[4];
    int n_pools = 0;
    int total = 0;

    if (flags & PASSGEN_SYMBOLS) { pools[n_pools] = SYM; pool_sizes[n_pools] = std::strlen(SYM); total += pool_sizes[n_pools]; n_pools++; }
    if (flags & PASSGEN_NUMBERS) { pools[n_pools] = NUM; pool_sizes[n_pools] = std::strlen(NUM); total += pool_sizes[n_pools]; n_pools++; }
    if (flags & PASSGEN_UPPER)   { pools[n_pools] = UPP; pool_sizes[n_pools] = std::strlen(UPP); total += pool_sizes[n_pools]; n_pools++; }
    if (flags & PASSGEN_LOWER)   { pools[n_pools] = LOW; pool_sizes[n_pools] = std::strlen(LOW); total += pool_sizes[n_pools]; n_pools++; }

    if (n_pools == 0) {
        pools[0] = UPP; pool_sizes[0] = std::strlen(UPP); total += pool_sizes[0]; n_pools++;
        pools[1] = LOW; pool_sizes[1] = std::strlen(LOW); total += pool_sizes[1]; n_pools++;
    }

    int cumsum[4];
    int running = 0;
    for (int i = 0; i < n_pools; i++) {
        running += pool_sizes[i];
        cumsum[i] = running;
    }

    unsigned char* randbuf = new unsigned char[length];
    if (!get_rand(randbuf, length)) {
        delete[] randbuf;
        return -2;
    }

    for (int i = 0; i < length; i++) {
        int r = randbuf[i] % total;
        for (int j = 0; j < n_pools; j++) {
            if (r < cumsum[j]) {
                int idx = (randbuf[i] + i) % pool_sizes[j];
                out[i] = pools[j][idx];
                break;
            }
        }
    }
    out[length] = '\0';

    delete[] randbuf;
    return length;
}
