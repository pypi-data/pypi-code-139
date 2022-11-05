'''
# Ethereum on Amazon Managed Blockchain

![license](https://img.shields.io/github/license/cdklabs/cdk-ethereum-node?color=green)
![release](https://img.shields.io/github/v/release/cdklabs/cdk-ethereum-node?color=green)
![npm:version](https://img.shields.io/npm/v/@cdklabs/cdk-ethereum-node?color=blue)
![PyPi:version](https://img.shields.io/pypi/v/cdklabs.cdk-ethereum-node?color=blue)
![Maven:version](https://img.shields.io/maven-central/v/io.github.cdklabs/cdk-ethereum-node?color=blue&label=maven)
![NuGet:version](https://img.shields.io/nuget/v/Cdklabs.CdkEthereumNode?color=blue)

This repository contains a CDK construct to deploy an Ethereum node running
on Amazon Managed Blockchain. The following networks are supported:

* Mainnet (default)
* Testnet: Ropsten
* Testnet: Rinkeby

<!-- TODO: add a documentation note here about Goerli network -->

## Installation

Note that this construct requires [AWS CDK v2](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install).

#### JavaScript

```bash
npm install --save @cdklabs/cdk-ethereum-node
```

#### Python

```bash
pip3 install cdklabs.cdk-ethereum-node
```

#### Java

Add the following to `pom.xml`:

```xml
<dependency>
  <groupId>io.github.cdklabs</groupId>
  <artifactId>cdk-ethereum-node</artifactId>
</dependency>
```

#### .NET

```bash
dotnet add package Cdklabs.CdkEthereumNode
```

## Usage

A minimally complete deployment is shown below. By default,
a `bc.t3.large` node will be created on the Ethereum Mainnet.

```python
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { EthereumNode } from '@cdklabs/cdk-ethereum-node';

export class MyStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    new EthereumNode(this, 'Example');
  }
}
```

The equivalent Python code is as follows:

```python
from aws_cdk import Stack
from cdklabs.cdk_ethereum_node import EthereumNode

class MyStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)
        EthereumNode(self, 'Example')
```

The following is a more complex instantiation illustrating some of the node configuration options available.

```python
new EthereumNode(this, 'Example', {
  networkType: NetworkId.ROPSTEN,
  availabilityZone: 'us-east-1b',
  instanceType: InstanceType.BURSTABLE3_LARGE,
});
```

The following provides an example of how to leverage the construct to deploy more than one node at a time.

```python
for (const i = 0; i < 10; i++) {
  new EthereumNode(this, `Example_${i}`);
}
```

See the [API Documentation](API.md) for details on all available input and output parameters.

## References

* [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
* [Amazon Managed Blockchain](https://aws.amazon.com/managed-blockchain/)
* [Ethereum](https://ethereum.org/en/developers/docs/)

## Contributing

Pull requests are welcomed. Please review the [Contributing Guidelines](CONTRIBUTING.md)
and the [Code of Conduct](CODE_OF_CONDUCT.md).

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## Authors

* Trinity Key (trinikey@amazon.com)
* Marc Gozali (gozalim@amazon.com)

## License

This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs


class EthereumNode(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/cdk-ethereum-node.EthereumNode",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["InstanceType"] = None,
        network: typing.Optional["Network"] = None,
    ) -> None:
        '''Creates an Ethereum public network node on an Amazon Managed Blockchain network.

        :param scope: -
        :param id: -
        :param availability_zone: The Availability Zone in which the node will be created. Default: - us-east-1a
        :param instance_type: The Amazon Managed Blockchain instance type for the Ethereum node. Default: - BURSTABLE3_LARGE
        :param network: The Ethereum Network in which the node will be created. Default: - The default network selected is Mainnet network
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                availability_zone: typing.Optional[builtins.str] = None,
                instance_type: typing.Optional["InstanceType"] = None,
                network: typing.Optional["Network"] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EthereumNodeProps(
            availability_zone=availability_zone,
            instance_type=instance_type,
            network=network,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        '''The Availability Zone in which the node exists.'''
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> "InstanceType":
        '''The Amazon Managed Blockchain instance type for the node.'''
        return typing.cast("InstanceType", jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "Network":
        '''Managed Blockchain Ethereum network identifier.'''
        return typing.cast("Network", jsii.get(self, "network"))


@jsii.data_type(
    jsii_type="@cdklabs/cdk-ethereum-node.EthereumNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "instance_type": "instanceType",
        "network": "network",
    },
)
class EthereumNodeProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["InstanceType"] = None,
        network: typing.Optional["Network"] = None,
    ) -> None:
        '''Construct properties for ``EthereumNode``.

        :param availability_zone: The Availability Zone in which the node will be created. Default: - us-east-1a
        :param instance_type: The Amazon Managed Blockchain instance type for the Ethereum node. Default: - BURSTABLE3_LARGE
        :param network: The Ethereum Network in which the node will be created. Default: - The default network selected is Mainnet network
        '''
        if __debug__:
            def stub(
                *,
                availability_zone: typing.Optional[builtins.str] = None,
                instance_type: typing.Optional["InstanceType"] = None,
                network: typing.Optional["Network"] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
        self._values: typing.Dict[str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if network is not None:
            self._values["network"] = network

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone in which the node will be created.

        :default: - us-east-1a
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional["InstanceType"]:
        '''The Amazon Managed Blockchain instance type for the Ethereum node.

        :default: - BURSTABLE3_LARGE
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["InstanceType"], result)

    @builtins.property
    def network(self) -> typing.Optional["Network"]:
        '''The Ethereum Network in which the node will be created.

        :default: - The default network selected is Mainnet network
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["Network"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EthereumNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdklabs/cdk-ethereum-node.InstanceType")
class InstanceType(enum.Enum):
    '''Supported instance types for Managed Blockchain nodes.'''

    BURSTABLE3_SMALL = "BURSTABLE3_SMALL"
    BURSTABLE3_MEDIUM = "BURSTABLE3_MEDIUM"
    BURSTABLE3_LARGE = "BURSTABLE3_LARGE"
    BURSTABLE3_XLARGE = "BURSTABLE3_XLARGE"
    STANDARD5_LARGE = "STANDARD5_LARGE"
    STANDARD5_XLARGE = "STANDARD5_XLARGE"
    STANDARD5_XLARGE2 = "STANDARD5_XLARGE2"
    STANDARD5_XLARGE4 = "STANDARD5_XLARGE4"
    COMPUTE5_LARGE = "COMPUTE5_LARGE"
    COMPUTE5_XLARGE = "COMPUTE5_XLARGE"
    COMPUTE5_XLARGE2 = "COMPUTE5_XLARGE2"
    COMPUTE5_XLARGE4 = "COMPUTE5_XLARGE4"


@jsii.enum(jsii_type="@cdklabs/cdk-ethereum-node.Network")
class Network(enum.Enum):
    '''Supported Ethereum networks for Managed Blockchain nodes.'''

    MAINNET = "MAINNET"
    ROPSTEN = "ROPSTEN"
    RINKEBY = "RINKEBY"


__all__ = [
    "EthereumNode",
    "EthereumNodeProps",
    "InstanceType",
    "Network",
]

publication.publish()
