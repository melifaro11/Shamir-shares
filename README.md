# Shamir's Secret Sharing

Simple python implementation of Shamir's Secret Sharing algorithm: https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing

## Usage

### Import library
```python
from secret_sharing import ShamirSharing
```

### Create share

Create share secret with (2, 4) threshold scheme and auto key length

```python
shamir = ShamirSharing()
keys = s.split_secret('Hallo world', 2, 4)
```

Output:

```bash
[(1, 68724745325519546275944861460257),
 (2, 136574463364809580625387577920503),
 (3, 42164904574886251583252284092622),
 (4, 110014622614176285932695000552868)]
```

The split_secret() function encodes the input text into an integer. The key length in this case depends on the length of the encoded secret, and is determined by nearest bigger prime number, which is selected from predifined set (Mersenne numbers). The key length can be set explicitly using the KeyOrder.MERSENNE_* constants.

```python
shamir = ShamirSharing()
keys = s.split_secret('Hallo world', 2, 4, key_order=KeyOrder.MERSENNE_521)
```

Output:

```bash
[(1, 3056702466373401763663765074593114490479434886942244541120592965312149867906931239906752800072112402534778360081117991188485398813340795775706081476717448313),
 (2, 6113404932746803527327530149186228980958869773884489082241185930624299735813862479813505600144224805069556720162235982376970796751654305321900236451289896615),
 (3, 2305309738989595576009394424697950254168869360683428213967315436750906420323137667597698759554882652627038768851873115528334206690251171055520363134747287766),
 (4, 5362012205362997339673159499291064744648304247625672755087908402063056288230068907504451559626995055161817128932991106716819604628564680601714518109319736068)]
```

<i>Note: if the prime number is not long enough to encode the message, an exception ValueError is thrown</i>

Below is a table with all KeyOrder.MERSENNE_* constants

| #  | Name             | Mersene number           | Digits
|----|------------------|--------------------------|----------------------
| 1  | MERSENNE_13      | 2<sup>13</sup> - 1       | 4
| 2  | MERSENNE_17      | 2<sup>17</sup> - 1       | 6
| 3  | MERSENNE_19      | 2<sup>19</sup> - 1       | 6
| 4  | MERSENNE_31      | 2<sup>31</sup> - 1       | 10
| 5  | MERSENNE_61      | 2<sup>61</sup> - 1       | 19
| 6  | MERSENNE_89      | 2<sup>89</sup> - 1       | 27
| 7  | MERSENNE_107     | 2<sup>107</sup> - 1      | 33
| 8  | MERSENNE_127     | 2<sup>127</sup> - 1      | 39
| 9  | MERSENNE_521     | 2<sup>521</sup> - 1      | 157
| 10 | MERSENNE_607     | 2<sup>607</sup> - 1      | 183
| 11 | MERSENNE_1279    | 2<sup>1279</sup> - 1     | 386
| 12 | MERSENNE_2203    | 2<sup>2203</sup> - 1     | 664
| 13 | MERSENNE_2281    | 2<sup>2281</sup> - 1     | 687
| 14 | MERSENNE_3127    | 2<sup>3127</sup> - 1     | 969
| 15 | MERSENNE_4253    | 2<sup>4253</sup> - 1     | 1281
| 16 | MERSENNE_4423    | 2<sup>4423</sup> - 1     | 1332
| 17 | MERSENNE_9689    | 2<sup>9689</sup> - 1     | 2917

### Recover share

```python
shamir.recover_secret([keys[0], keys[2]]))
```

```python
shamir.recover_secret([
        (1, 68724745325519546275944861460257),
        (3, 42164904574886251583252284092622)
    ])
```

Output:
```bash
'Hallo world'
```

recover_secret() returns decoded string or None, if decode error (invalid keys)